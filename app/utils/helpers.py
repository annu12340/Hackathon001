import logging
from typing import Dict, Any
import json
from datetime import datetime
import os

logger = logging.getLogger(__name__)

def parse_slack_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Parse and validate Slack event data."""
    try:
        # Verify event type
        event_type = event.get("type")
        if event_type != "event_callback":
            raise ValueError(f"Unexpected event type: {event_type}")

        # Extract inner event
        inner_event = event.get("event", {})
        if not inner_event:
            raise ValueError("No inner event found")

        # Verify event subtype
        if inner_event.get("subtype") == "bot_message":
            return None  # Ignore bot messages

        return inner_event
    except Exception as e:
        logger.error(f"Error parsing Slack event: {str(e)}")
        raise

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display."""
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception as e:
        logger.error(f"Error formatting timestamp: {str(e)}")
        return timestamp
