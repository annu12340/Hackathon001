import logging
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from . import config
from .triage import TriageService
from .azure.databricks_client import DatabricksTriageClient
from .utils.log_collector import LogCollector
logger = logging.getLogger(__name__)
databricks_client = DatabricksTriageClient(use_mock=True)

class SlackBot:
    def __init__(self):
        self.app = AsyncApp(token=config.SLACK_BOT_TOKEN)
        self.triage_service = TriageService()
        self.log_collector = LogCollector()
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.event("message")
        async def handle_message(event, say):
            if event.get("subtype") == "bot_message":
                return

            text = event.get("text", "")
            thread_ts = event.get("thread_ts", event.get("ts"))

            if "PagerDuty" in text:
                await self.handle_alert(text, thread_ts, say)

    async def handle_alert(self, text: str, thread_ts: str, say):
        try:
            await say(text="🔍 Analyzing alert...", thread_ts=thread_ts)
            
            node_id = "lima-rancher-desktop"

            # Collect diagnostics
            diagnostics = await self.log_collector.collect_all_diagnostics(host=node_id)
            
            # Format and send the report
            report = self.log_collector.format_diagnostics_report(diagnostics)
            
            # Split report into chunks if it's too long for Slack
            max_length = 3900  # Slack has a 4000 character limit
            chunks = [report[i:i + max_length] for i in range(0, len(report), max_length)]
            
            for i, chunk in enumerate(chunks):
                await say(
                    text=f"```{chunk}```",
                    thread_ts=thread_ts
                )
            # Get triage steps and convert to proper format
            # triage_steps = databricks_client.get_triage_steps(node_id)
            

            # # Run triage steps
            # results = await self.triage_service.orchestrate_triage(triage_steps)
            
            # await self.send_results(results, node_id, thread_ts, say)
            
        except Exception as e:
            logger.error(f"Error handling alert: {e}")
            await say(text=f"Error: {str(e)}", thread_ts=thread_ts)

    async def send_results(self, results: dict, node_id: str, thread_ts: str, say):
        try:
            # Count successful steps
            success_count = sum(1 for platform in results.values() 
                              for step in platform["steps_results"] 
                              if step["status"] == "success")
            total_steps = sum(len(platform["steps_results"]) for platform in results.values())
            
            # Format message
            message = [
                f"*Triage Results for `{node_id}`*",
                f"Success Rate: {success_count}/{total_steps}\n"
            ]
            
            for platform, platform_data in results.items():
                message.append(f"*Platform: {platform}*")
                for step in platform_data["steps_results"]:
                    status = "✅" if step["status"] == "success" else "❌"
                    message.append(f"{status} `{step['step']}`")
                    if "output" in step:
                        output = step["output"][:1000] if step["output"] else "No output"
                        message.append(f"```{output}```")
                message.append("")
            
            await say(text="\n".join(message), thread_ts=thread_ts)
        except Exception as e:
            logger.error(f"Error formatting results: {e}")
            await say(text="Error formatting triage results", thread_ts=thread_ts)

    async def start(self):
        handler = AsyncSocketModeHandler(
            app_token=config.SLACK_APP_TOKEN,
            app=self.app
        )
        await handler.start_async() 