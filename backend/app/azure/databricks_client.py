import os
import sys
import logging
import requests
import json
import subprocess
import asyncio
from typing import Dict, List, Tuple
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.log_collector import LogCollector

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
        self.log_collector = LogCollector()
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

    def get_triage_steps(self, cluster: str, node_id: str, summarized_pd_alert, logs) -> Dict[str, List[str]]:
        """Fetch triage steps from Databricks for a specific node."""
        try:
            message = f"""
            PagerDuty: {summarized_pd_alert}
            Log summary: {logs.get('issue_found_in_logs')}
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

    def get_logs(self, cluster: str, node_id: str, log_type: str = "all", time_range: str = "last_hour") -> Dict:
        """
        Collect logs based on the platform type.
        """
        try:
            logger.info(f"Collecting logs for node {node_id} in cluster {cluster}")
            
            # Determine the number of lines to collect based on time range
            lines = 100
            if time_range == "last_day":
                lines = 1000
            elif time_range == "last_week":
                lines = 5000
                
            # Collect logs using the LogCollector
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Collect system info and logs
            diagnostics = loop.run_until_complete(
                self.log_collector.collect_all_diagnostics(node_id)
            )
            
            # Filter logs based on log_type if needed
            if log_type != "all":
                filtered_logs = {}
                for log_file, content in diagnostics.get("logs", {}).items():
                    if log_type in log_file.lower():
                        filtered_logs[log_file] = content
                diagnostics["logs"] = filtered_logs
            
            logger.info(f"Successfully collected logs for node {node_id}")
            return diagnostics
            
        except Exception as e:
            logger.error(f"Error collecting logs: {str(e)}")
            raise

    def get_and_analyze_logs(self, cluster: str, node_id: str, platform: str,  time_range: str = "last_hour") -> Dict:
        """
        Get and analyze logs for a specific node.
        """
        try:
            # Collect logs
            logs = self.get_logs(cluster, node_id,time_range)
            # Create a message for the Databricks API
            message = f""" Logs: {logs} """

            # Call the Databricks API
            response = self.score_model(message)
            result = response['messages'][0]['content']
            logger.info(f"Successfully analyzed logs for node {node_id} with result {result}")
            return result

        except Exception as e:
            logger.error(f"Error analyzing logs: {str(e)}")
            raise

    def execute_triage_step(self,step: str) -> Dict:
        """Execute a single triage step with safety checks."""
        try:
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
                    "output": output
                }
            except subprocess.TimeoutExpired:
                return {
                    "status": "error",
                    "message": f"Command timed out after {self.command_timeout} seconds",
                    "step": step,
                }
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode('utf-8').strip() if e.stderr else "Command failed with no error message"
                return {
                    "status": "error",
                    "message": error_msg,
                    "step": step,
                    "output": e.stdout.decode('utf-8').strip() if e.stdout else "",
                    "error": error_msg,
   
                }
            
        except Exception as e:
            logger.error(f"Error executing step: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "step": step
            }

    async def orchestrate_triage(self, cluster, node_id, triage_steps, say, thread_ts) -> Dict:
        """Orchestrate triage steps by executing commands and posting Slack messages."""
        results = {"blocks": []}
        

        def format_risk(risk: str) -> str:
            emoji = {"low": ":priority-low:", "medium": ":priority-medium:", "high": ":priority-highest:"}
            return f"{emoji.get(risk, '❔')} *{risk.upper()}* risk"

        def create_section(text: str) -> Dict:
            return {"type": "section", "text": {"type": "mrkdwn", "text": text}}
        
        for step in triage_steps.get("actions", []):
            command = step.get("command")
            risk = step.get("risk", "unknown")

            blocks=[create_section(f"- Executing command `{command}` with {format_risk(risk)}")]

            if risk in ("low", "medium"):
                result = self.execute_triage_step(command)

                if result["status"] == "error":
                    blocks.append(create_section(f"❌ *Error:* {result.get('message', 'Unknown error')}"))
                    await say(blocks=blocks, thread_ts=thread_ts)
                    break

            elif risk == "high":
                blocks.append(create_section(f"Since this is a high risk command, human in the loop is required"))
                blocks.append({
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Approve", "emoji": True},
                            "value": f"execute_{command}",
                            "action_id": "execute_high_risk_command",
                            "style": "danger"
                        }
                    ]
                })
                

            await say(blocks=blocks, thread_ts=thread_ts)

        return results

