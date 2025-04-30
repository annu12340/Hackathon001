import logging
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from . import config
from .incident_manager import IncidentManager
import subprocess

logger = logging.getLogger(__name__)

class SlackBot:
    def __init__(self):
        self.app = AsyncApp(token=config.SLACK_BOT_TOKEN)
        self.incident_manager = IncidentManager(self.app, config)
        self.setup_handlers()

    def setup_handlers(self):

        @self.app.event("message")
        async def handle_message(event, say):
            if event.get("subtype") == "bot_message":
                return

            text = event.get("text", "")
            thread_ts = event.get("thread_ts", event.get("ts"))
            # Check if this is a PagerDuty alert in Slack
            if config.PAGERDUTY_URL in text:
                print("PagerDuty alert detected. The text is",text)
                await self.handle_alert(text, thread_ts, say)

        
        @self.app.event("app_mention")
        async def handle_app_mention(event, say):
            print("App is mentioned")
        
        @self.app.action("execute_high_risk_command")
        async def handle_high_risk_command(ack, body, say, logger):
            await ack()
            logger.info(body)
            
            value = body["actions"][0]["value"]
            command = value.replace("execute_", "")  
            thread_ts = body["container"]["thread_ts"]
            
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=self.command_timeout
                )
                output = result.stdout.decode('utf-8').strip()
                return {
                    "status": "success",
                    "message": "Step executed successfully",
                    "step": command,
                    "output": output
                }
            except subprocess.TimeoutExpired:
                return {
                    "status": "error",
                    "message": f"Command timed out after {self.command_timeout} seconds",
                    "step": command,
                }
            
    async def start(self):
        handler = AsyncSocketModeHandler(
            app_token=config.SLACK_APP_TOKEN,
            app=self.app
        )
        print("handler", handler)
        await handler.start_async() 