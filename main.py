import os
import logging
import asyncio
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from app.triage_agent import TriageAgent
from app.databricks_client import DatabricksTriageClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize components
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
triage_agent = TriageAgent()
databricks_client = DatabricksTriageClient(use_mock=True)

@app.event("message")
def handle_message(event, say):
    """Handle incoming messages and process PagerDuty alerts."""
    try:
        # Skip if the message is from a bot
        if event.get("subtype") == "bot_message":
            return

        # Get message text
        text = event.get("text", "")
        thread_ts = event.get("thread_ts", event.get("ts"))

        # Check if this is a PagerDuty alert
        if "PagerDuty" in text:
            say(text="🔍 Analyzing alert and fetching runbook steps...", thread_ts=thread_ts)
            
            # Create event loop for async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # TODO: Extract node ID from the alert
                # Extract node ID from the alert (example: k8s-node-001)
                node_id = "lima-rancher-desktop"  # This should be extracted from the actual alert
                
                # Get triage steps (synchronous call)
                triage_steps = databricks_client.get_triage_steps(node_id)
                
                # Execute triage steps (async call)
                results = loop.run_until_complete(triage_agent.orchestrate_triage(triage_steps))
                
                # Format response
                if results:
                    success_count = sum(1 for platform in results.values() 
                                      for step in platform["steps_results"] 
                                      if step["status"] == "success")
                    total_steps = sum(len(platform["steps_results"]) for platform in results.values())
                    
                    response = [
                        f"*Triage Results for `{node_id}`*",
                        f"Success Rate: {success_count}/{total_steps}",
                        ""
                    ]
                    
                    for platform, platform_results in results.items():
                        response.append(f"*Platform: {platform}*")
                        for step in platform_results["steps_results"]:
                            status = "✅" if step["status"] == "success" else "❌"
                            output = step["output"]
                            response.append(f"{status} `{step['step']}`")
                            response.append(f"Output: \n ```{output[:100]}```")
                        response.append("")
                    
                    say(text="\n".join(response), thread_ts=thread_ts)
                else:
                    say(text="No triage steps found for this alert.", thread_ts=thread_ts)
            finally:
                loop.close()

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        say(text=f"Error processing alert: {str(e)}", thread_ts=thread_ts)

if __name__ == "__main__":
    handler = SocketModeHandler(app_token=os.environ.get("SLACK_APP_TOKEN"), app=app)
    handler.start()