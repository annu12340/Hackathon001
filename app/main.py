import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from app.azure.search import RunbookSearch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Initialize Azure search
runbook_search = RunbookSearch()

@app.event("message")
def handle_message(event, say):
    """Handle incoming messages and process PagerDuty alerts."""
    try:
        # Skip if the message is from a bot
        if event.get("subtype") == "bot_message":
            return

        # Get message text
        text = event.get("text", "")
        channel = event.get("channel")
        thread_ts = event.get("thread_ts")

        # Check if this is a PagerDuty alert
        if "PagerDuty" in text:
            # Search for relevant runbooks
            runbooks = runbook_search.search_runbooks(text)
            
            if runbooks:
                # Format and send the response
                response = format_runbook_response(runbooks[0])
                say(text=response, thread_ts=thread_ts)
            else:
                say(text="No relevant runbook found for this alert.", thread_ts=thread_ts)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        say(text=f"Error processing alert: {str(e)}", thread_ts=thread_ts)

def format_runbook_response(runbook):
    """Format runbook content for Slack response."""
    return f"""
*{runbook['title']}*
Category: {runbook['category']}
Severity: {runbook['severity']}

{runbook['content']}
"""

# Start the app
if __name__ == "__main__":
    # Initialize socket mode handler
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start() 