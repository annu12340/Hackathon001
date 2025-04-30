import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

def get_required_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise ValueError(f"Required environment variable {key} is not set")
    return value

# Slack configuration
SLACK_BOT_TOKEN = get_required_env("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = get_required_env("SLACK_APP_TOKEN")

# PagerDuty configuration
PAGERDUTY_API_KEY = get_required_env("PAGERDUTY_API_KEY")
PAGERDUTY_URL = get_required_env("PAGERDUTY_URL")

# Azure Databricks configuration
AZURE_DATABRICKS_ENDPOINT = get_required_env("AZURE_DATABRICKS_ENDPOINT")
AZURE_DATABRICKS_TOKEN = get_required_env("AZURE_DATABRICKS_TOKEN")
AZURE_DATABRICKS_WAREHOUSE_ID = get_required_env("AZURE_DATABRICKS_WAREHOUSE_ID")

# MongoDB configuration
AZURE_COSMO_DB = get_required_env("AZURE_COSMO_DB")
MONGO_DB_NAME = get_required_env("MONGO_DB_NAME")

# Command execution settings
COMMAND_TIMEOUT = int(os.environ.get("COMMAND_TIMEOUT", "300"))

