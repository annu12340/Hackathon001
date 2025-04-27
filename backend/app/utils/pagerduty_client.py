import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PagerDutyClient:
    def __init__(self, api_key):
        """
        Initialize the PagerDuty client with API key
        
        Args:
            api_key (str): PagerDuty API key
        """
        self.api_key = api_key
        self.base_url = "https://api.pagerduty.com"
        self.headers = {
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Authorization": f"Token token={api_key}",
            "Content-Type": "application/json"
        }
    
    def get_incident(self, incident_id):
        """
        Get details of a specific incident from PagerDuty
        
        Args:
            incident_id (str): The PagerDuty incident ID
            
        Returns:
            dict: Incident details or None if API call failed
        """
        try:
            url = f"{self.base_url}/incidents/{incident_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()["incident"]
            else:
                logger.error(f"Failed to get incident {incident_id}: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.exception(f"Error getting incident {incident_id}: {str(e)}")
            return None
    
    def format_incident_details(self, incident):
        """
        Format incident details into a readable message
        
        Args:
            incident (dict): The incident details from PagerDuty
            
        Returns:
            str: Formatted incident details
        """
        if not incident:
            return "❌ Could not retrieve incident details"
        
        # Extract useful fields
        id = incident.get("id", "Unknown")
        title = incident.get("title", "Unknown")
        status = incident.get("status", "Unknown").upper()
        urgency = incident.get("urgency", "Unknown").upper()
        
        # Format created and last updated times
        created_at = incident.get("created_at")
        last_updated = incident.get("last_status_change_at")
        
        if created_at:
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            created_at = "Unknown"
            
        if last_updated:
            last_updated = datetime.fromisoformat(last_updated.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            last_updated = "Unknown"
            
        # Get assignee information
        assignees = incident.get("assignments", [])
        assignee_text = "Unassigned"
        if assignees:
            assignee_names = [a.get("assignee", {}).get("summary", "Unknown") for a in assignees]
            assignee_text = ", ".join(assignee_names)
        
        # Format incident details
        incident_url = incident.get("html_url", "#")
        service_name = incident.get("service", {}).get("summary", "Unknown")
        
        # Create formatted message for Slack
        status_emoji = "🔴" if status == "TRIGGERED" else "🟡" if status == "ACKNOWLEDGED" else "🟢"
        urgency_emoji = "🔥" if urgency == "HIGH" else "⚠️"
        
        formatted_message = [
            f"*PagerDuty Incident {id}*",
            f"{status_emoji} *Status:* {status}",
            f"{urgency_emoji} *Urgency:* {urgency}",
            f"*Title:* {title}",
            f"*Service:* {service_name}",
            f"*Created:* {created_at}",
            f"*Last Updated:* {last_updated}",
            f"*Assigned to:* {assignee_text}",
            f"*Details:* <{incident_url}|View in PagerDuty>"
        ]
        
        return "\n".join(formatted_message) 