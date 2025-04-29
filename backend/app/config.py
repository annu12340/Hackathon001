import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Slack configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
PAGERDUTY_URL="https://abcqwerty1.pagerduty.com"

# PagerDuty configuration
PAGERDUTY_API_KEY = os.environ.get("PAGERDUTY_API_KEY")

# Command execution settings
COMMAND_TIMEOUT = 300  

