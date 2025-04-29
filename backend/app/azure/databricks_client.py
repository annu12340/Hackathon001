import os
import logging
import requests
import json
import subprocess
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()

logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

class DatabricksTriageClient:
    def __init__(self):
        self.api_url = os.getenv("AZURE_DATABRICKS_ENDPOINT")
        self.headers = {
            'Authorization': f'Bearer {os.getenv("AZURE_DATABRICKS_TOKEN")}',
            'Content-Type': 'application/json'
        }
        logger.info("Initialized DatabricksTriageClient")

    def create_request_data(self, message: str) -> Dict:
        """Create the request data structure for the API call."""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "context": {
                "conversation_id": "test_conversation",
                "user_id": "test_user"
            }
        }



    def score_model(self, message: str) -> Dict:
        """Make an API call to the Databricks endpoint."""
        try:
            data = self.create_request_data(message)
            data_json = json.dumps(data)
            
            response = requests.request(
                method='POST',
                headers=self.headers,
                url=self.api_url,
                data=data_json
            )
            
            if response.status_code != 200:
                raise Exception(f'Request failed with status {response.status_code}, {response.text}')
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Error in score_model: {str(e)}")
            raise

    def get_triage_steps(self,cluster: str, node_id: str, summarized_pd_alert) -> Dict[str, List[str]]:
        """Fetch triage steps from Databricks for a specific node. """
        try:
            message = f"""
            PagerDuty: {summarized_pd_alert}
            """
            response = self.score_model(message)
            raw_string = response['messages'][0]['content']
            # print("Raw string is", raw_string)
            json_string = raw_string.strip("`json\n").rstrip("`")
            parsed_data = json.loads(json_string)
            logger.info(f"Successfully fetched triage steps: {parsed_data}")
            return parsed_data

        except Exception as e:
            logger.error(f"Error fetching triage steps: {str(e)}", 
                        extra={"node_id": node_id})
            raise 
