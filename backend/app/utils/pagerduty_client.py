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
                incident = response.json()["incident"]
                print("incidentincidentincident",incident)
                return incident
            else:
                logger.error(f"Failed to get incident {incident_id}: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.exception(f"Error getting incident {incident_id}: {str(e)}")
            return None
        
    def format_incident_details(self, summary):
        """
        Format the incident summary dict into a Slack-friendly message.
        """
        return (
            f"*Status:* {summary.get('Status', 'N/A')}\n"
            f"*Urgency:* {summary.get('Urgency', 'N/A')}\n"
            f"*Title:* {summary.get('Title', 'N/A')}\n"
            f"*Time (UTC):* {summary.get('Time_UTC', 'N/A')}\n"
            f"*Summary of the Issue:* {summary.get('Summary_of_the_Issue', 'N/A')}\n"
            f"*Environment/Cluster:* {summary.get('Environment_or_Cluster', 'N/A')}\n"
            f"*Host/Node Name:* {summary.get('Host_or_Node_Name', 'N/A')}\n"
            f"*Error Type:* {summary.get('Error_Type', 'N/A')}\n"
            f"*Impacted Component:* {summary.get('Impacted_Component', 'N/A')}\n"
            f"*Time:* {summary.get('Time', 'N/A')}"
        )