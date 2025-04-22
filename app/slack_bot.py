import logging
import asyncio
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

    async def update_status(self, channel, ts, steps_done, current_step, thread_ts):
        emojis = [":white_check_mark:" if i < steps_done else ":loading-dot:" if i == steps_done else "▫️" 
                  for i in range(4)]
        messages = [
            f"{emojis[0]} Alert analyzed",
            f"{emojis[1]} Triage steps fetched",
            f"{emojis[2]} Diagnostics complete",
            f"{emojis[3]} Formatting results..."
        ]
        await self.app.client.chat_update(
            channel=channel,
            ts=ts,
            text="\n".join(messages),
            thread_ts=thread_ts
        )

    async def handle_alert(self, text: str, thread_ts: str, say):
        try:
            initial_message = await say(text=":loading-dot: Analyzing alert...", thread_ts=thread_ts)
            message_ts = initial_message['ts']
            channel = initial_message['channel']

            # Step 1: Analyze alert
            await asyncio.sleep(2)
            await self.update_status(channel, message_ts, steps_done=1, current_step="Analyzing alert", thread_ts=thread_ts)

            # Step 2: Get triage steps
            node_id = "lima-rancher-desktop"
            triage_steps = databricks_client.get_triage_steps(node_id)
            await asyncio.sleep(2)
            await self.update_status(channel, message_ts, steps_done=2, current_step="Fetching triage steps", thread_ts=thread_ts)

            # Step 3: Run diagnostics
            results = await self.triage_service.orchestrate_triage(triage_steps)
            await asyncio.sleep(2)
            await self.update_status(channel, message_ts, steps_done=3, current_step="Running diagnostics", thread_ts=thread_ts)
            
            print("\n\n\n results",results)
            # Step 4: Format results
            await self.send_results(results, node_id, thread_ts, say)
            await self.update_status(channel, message_ts, steps_done=4, current_step="Formatting results", thread_ts=thread_ts)

        except Exception as e:
            logger.exception("Error handling alert")
            if 'message_ts' in locals():
                await self.app.client.chat_update(
                    channel=channel,
                    ts=message_ts,
                    text=f":x: Error: {str(e)}",
                    thread_ts=thread_ts
                )

    async def send_results(self, results: dict, node_id: str, thread_ts: str, say):
        """Format and send triage results to Slack."""
        try:
            # Count successful steps
            success_count = 0
            total_steps = 0
            
            message = [
                f"*Triage Results for `{node_id}`*\n"
            ]
            
            for platform, platform_data in results.items():
                message.append(f"*Platform: {platform}*")
                
                # Handle steps_results for each platform
                steps = platform_data.get('steps_results', [])
                total_steps += len(steps)
                
                for step in steps:
                    status = "✅" if step.get("status") == "success" else "❌"
                    if step.get("status") == "success":
                        success_count += 1
                        
                    message.append(f"{status} `{step.get('step', 'Unknown step')}`")
                    
                    # Handle output or error message
                    if step.get("output"):
                        output = step["output"][:1000] if len(step["output"]) > 1000 else step["output"]
                        message.append(f"```{output}```")
                    elif step.get("error"):
                        message.append(f"```Error: {step['error']}```")
                
                message.append("")  # Add blank line between platforms
            
            # Add summary at the top
            message.insert(1, f"Success Rate: {success_count}/{total_steps}\n")
            
            await say(text="\n".join(message), thread_ts=thread_ts)
            
        except Exception as e:
            print(f"Error formatting results: {e}")
            await say(text=f"Error formatting results: {str(e)}", thread_ts=thread_ts)

    async def start(self):
        handler = AsyncSocketModeHandler(
            app_token=config.SLACK_APP_TOKEN,
            app=self.app
        )
        await handler.start_async()
