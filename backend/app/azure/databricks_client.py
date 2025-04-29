import os
import logging
import requests
import json
import subprocess
from typing import Dict, List, Tuple
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
        self.command_timeout = 300
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

    def get_triage_steps(self, cluster: str, node_id: str, summarized_pd_alert) -> Dict[str, List[str]]:
        """Fetch triage steps from Databricks for a specific node."""
        try:
            message = f"""
            PagerDuty: {summarized_pd_alert}
            """
            response = self.score_model(message)
            raw_string = response['messages'][0]['content']
            json_string = raw_string.strip("`json\n").rstrip("`")
            parsed_data = json.loads(json_string)
            logger.info(f"Successfully fetched triage steps: {parsed_data}")
            return parsed_data
        except Exception as e:
            logger.error(f"Error getting triage steps: {str(e)}")
            raise

    def analyze_triage_steps(self, platform: str, steps: List[str]) -> Dict:
        """Analyze triage steps using Azure Databricks."""
        try:
            message = f"""
            Analyze the following triage steps for {platform} platform:
            {json.dumps(steps)}
            
            Provide:
            1. Risk assessment for each step
            2. Expected outcome
            3. Potential failure scenarios
            4. Recovery steps if something goes wrong
            
            Format the response as JSON.
            """
            
            response = self.score_model(message)
            raw_string = response['messages'][0]['content']
            json_string = raw_string.strip("`json\n").rstrip("`")
            analysis = json.loads(json_string)
            
            logger.info(f"Step analysis completed for {platform} with analysis: {analysis}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing steps: {str(e)}")
            raise

    def execute_triage_step(self, platform: str, step: str) -> Dict:
        """Execute a single triage step with safety checks."""
        try:
            # Analyze the step before execution
            analysis = self.analyze_triage_steps(platform, [step])
            
            # If risk is too high, require manual approval
            if analysis.get("risk_level") == "high":
                return {
                    "status": "pending_approval",
                    "message": "High-risk command requires manual approval",
                    "step": step,
                    "analysis": analysis
                }
            
            # Execute the command
            logger.info(f"Executing step: {step}")
            try:
                result = subprocess.run(
                    step,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=self.command_timeout
                )
                output = result.stdout.decode('utf-8').strip()
                return {
                    "status": "success",
                    "message": "Step executed successfully",
                    "step": step,
                    "output": output,
                    "analysis": analysis
                }
            except subprocess.TimeoutExpired:
                return {
                    "status": "error",
                    "message": f"Command timed out after {self.command_timeout} seconds",
                    "step": step,
                    "analysis": analysis
                }
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode('utf-8').strip() if e.stderr else "Command failed with no error message"
                return {
                    "status": "error",
                    "message": error_msg,
                    "step": step,
                    "output": e.stdout.decode('utf-8').strip() if e.stdout else "",
                    "error": error_msg,
                    "analysis": analysis
                }
            
        except Exception as e:
            logger.error(f"Error executing step: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "step": step
            }

    def orchestrate_triage(self,cluster,node_id,triage_steps) -> Dict:
        """Orchestrate the entire triage process."""
        results = {}
        
        for platform, steps in triage_steps.items():
            platform_results = []
            # Execute steps sequentially
            for step in steps:
                result = self.execute_triage_step(platform, step)
                platform_results.append(result)
                
                # If a step fails, stop execution for this platform
                if result["status"] == "error":
                    logger.error(f"Stopping execution for {platform} due to error")
                    break
                    
            results[platform] = {
                "steps_results": platform_results}
            
        return results 
