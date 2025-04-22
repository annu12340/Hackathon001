import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Slack configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# Command execution settings
COMMAND_TIMEOUT = 300  

# Allowed commands per platform
ALLOWED_COMMANDS = {
    "k8s": ["systemctl", "kubectl", "journalctl"],
    "linux": ["echo", "curl"]
} 