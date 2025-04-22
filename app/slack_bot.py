import logging
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from . import config
from .triage import TriageService
from app.azure.databricks_client import DatabricksTriageClient

logger = logging.getLogger(__name__)


class SlackBot:
    def __init__(self):
        self.app = AsyncApp(token=config.SLACK_BOT_TOKEN)
        self.triage_service = TriageService()
        self.databricks_client = DatabricksTriageClient(use_mock=True)
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.event("message")
        async def handle_message(event, say):
            # Skip bot messages
            if event.get("subtype") == "bot_message":
                return

            text = event.get("text", "")
            thread_ts = event.get("thread_ts", event.get("ts"))

            # Handle PagerDuty alerts
            if "PagerDuty" in text:
                await self.handle_alert(text, thread_ts, say)

    async def handle_alert(self, text: str, thread_ts: str, say):
        try:
            await say(text="🔍 Analyzing alert...", thread_ts=thread_ts)
            
            # For demo, using fixed node ID
            node_id = "lima-rancher-desktop"

            # Get triage steps 
            triage_steps = self.databricks_client.get_triage_steps(node_id)
            
            # Run triage steps
            results = await self.triage_service.orchestrate_triage(triage_steps)
            
            # Format and send results
            await self.send_results(results, node_id, thread_ts, say)
            
        except Exception as e:
            logger.error(f"Error handling alert: {e}")
            await say(text=f"Error: {str(e)}", thread_ts=thread_ts)

    async def send_results(self, results: dict, node_id: str, thread_ts: str, say):
        """Format and send triage results to Slack."""
        # Count successful steps
        success_count = sum(1 for platform in results.values() 
                          for step in platform 
                          if step["status"] == "success")
        total_steps = sum(len(steps) for steps in results.values())
        
        # Format message
        message = [
            f"*Triage Results for `{node_id}`*",
            f"Success Rate: {success_count}/{total_steps}\n"
        ]
        
        for platform, steps in results.items():
            message.append(f"*Platform: {platform}*")
            for step in steps:
                status = "✅" if step["status"] == "success" else "❌"
                message.append(f"{status} `{step['step']}`")
                if "output" in step:
                    message.append(f"```{step['output'][:100]}```")
            message.append("")
        
        await say(text="\n".join(message), thread_ts=thread_ts)

    async def start(self):
        """Start the Slack bot."""
        handler = AsyncSocketModeHandler(
            app_token=config.SLACK_APP_TOKEN,
            app=self.app
        )
        await handler.start_async() 