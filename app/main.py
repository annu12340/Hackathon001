import os
import re
import json
import asyncio
import logging
from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from pythonjsonlogger import jsonlogger
from app.triage_agent import TriageAgent
from app.databricks_client import DatabricksTriageClient

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

class TriageOrchestrator:
    def __init__(self, use_mock: bool = True):
        self.agent = TriageAgent()
        self.databricks_client = DatabricksTriageClient(use_mock=use_mock)
    
    async def handle_node_triage(self, node_id: str):
        """
        Handle the complete node triage process.
        
        Args:
            node_id: The ID of the node requiring triage
        """
        try:
            # Step 1: Get triage steps from Databricks
            logger.info(f"Fetching triage steps for node {node_id}")
            triage_steps = await self.databricks_client.get_triage_steps(node_id)
            
            # Step 2: Use AI agent to orchestrate triage
            logger.info(f"Starting triage orchestration for node {node_id}")
            results = await self.agent.orchestrate_triage(triage_steps)
            
            # Step 3: Process results
            success_count = 0
            total_steps = sum(len(steps) for steps in triage_steps.values())
            
            summary = []
            for platform, platform_results in results.items():
                platform_summary = [f"*Platform: {platform}*"]
                for step_result in platform_results["steps_results"]:
                    status_emoji = "✅" if step_result["status"] == "success" else "⚠️" if step_result["status"] == "pending_approval" else "❌"
                    step_summary = f"{status_emoji} `{step_result['step']}`"
                    
                    if step_result["status"] == "success":
                        success_count += 1
                        if step_result.get('output'):
                            step_summary += f"\n```{step_result['output'][:1000]}```"
                    elif step_result["status"] == "pending_approval":
                        step_summary += "\n_Requires manual approval_"
                    elif step_result["status"] == "error":
                        step_summary += f"\n```{step_result.get('error', 'Unknown error')}```"
                    
                    platform_summary.append(step_summary)
                
                summary.extend(platform_summary)
                summary.append("")  # Empty line between platforms
            
            return {
                "success_rate": f"{success_count}/{total_steps}",
                "summary": "\n".join(summary),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error in triage process: {str(e)}", 
                        extra={"node_id": node_id})
            raise

class SlackPagerDutyHandler:
    def __init__(self, use_mock: bool = True):
        self.orchestrator = TriageOrchestrator(use_mock=use_mock)
        self.app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))
        
        # Setup event handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.app.event("message")
        async def handle_message(event, say):
            """Handle incoming messages and process PagerDuty alerts."""
            try:
                # Skip if the message is from a bot
                if event.get("subtype") == "bot_message":
                    return

                text = event.get("text", "")
                thread_ts = event.get("thread_ts", event.get("ts"))

                # Check if this is a PagerDuty alert
                if "PagerDuty" in text:
                    await say(text="🔍 Analyzing alert and fetching runbook steps...", thread_ts=thread_ts)
                    
                    # Extract node ID from the alert
                    # This regex pattern should be adjusted based on your actual PagerDuty alert format
                    node_match = re.search(r"((?:k8s|db|multi)-[\w-]+)", text)
                    if not node_match:
                        await say(text="❌ Could not identify node ID from the alert.", thread_ts=thread_ts)
                        return
                        
                    node_id = node_match.group(1)
                    
                    # Start triage process
                    await say(text=f"🚀 Starting triage for node `{node_id}`...", thread_ts=thread_ts)
                    
                    try:
                        result = await self.orchestrator.handle_node_triage(node_id)
                        
                        # Send summary message
                        header = [
                            f"*Triage Summary for `{node_id}`*",
                            f"Success Rate: {result['success_rate']}",
                            "",  # Empty line
                            result['summary']
                        ]
                        
                        await say(text="\n".join(header), thread_ts=thread_ts)
                        
                    except Exception as e:
                        await say(text=f"❌ Error during triage: {str(e)}", thread_ts=thread_ts)
                        
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await say(text=f"❌ Error processing alert: {str(e)}", thread_ts=thread_ts)

async def main():
    """Main entry point for the application."""
    # Initialize handler
    handler = SlackPagerDutyHandler(use_mock=True)
    
    # Initialize Socket Mode handler
    socket_handler = AsyncSocketModeHandler(
        app_token=os.environ.get("SLACK_APP_TOKEN"),
        app=handler.app
    )
    
    logger.info("Starting Slack app...")
    await socket_handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())