import os
import logging
import asyncio
from typing import Dict, List
# from databricks_api import DatabricksAPI
from pythonjsonlogger import jsonlogger

# Configure logging
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

class MockDatabricksResponse:
    """Mock response object for Databricks API calls."""
    def __init__(self, run_id: str):
        self.run_id = run_id
        
    @property
    def json(self):
        return {"run_id": self.run_id}
        
    def __getitem__(self, key):
        return self.json.get(key)

class DatabricksTriageClient:
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        logger.info(f"Initialized DatabricksTriageClient with mock={use_mock}")
        # if not use_mock:
            # self.client = DatabricksAPI(
            #     host=os.getenv("DATABRICKS_HOST"),
            #     token=os.getenv("DATABRICKS_TOKEN")
            # )
    
    async def _get_mock_triage_steps(self, node_id: str) -> Dict[str, List[str]]:
        """
        Generate mock triage steps based on node type.
        This is a placeholder implementation that returns predefined steps.
        """
        # Simulate API latency
        await asyncio.sleep(1)
        
        # Mock different scenarios based on node_id prefix
        if node_id.startswith("k8s"):
            return {
                "k8s": [
                    "kubectl get nodes",
                    "kubectl describe pod problem-pod",
                    "kubectl logs problem-pod",
                    "systemctl status kubelet",
                    "journalctl -u kubelet"
                ]
            }
        elif node_id.startswith("db"):
            return {
                "databricks": [
                    "databricks clusters list",
                    "databricks fs ls dbfs:/problems",
                    "curl -X GET https://your-workspace/api/2.0/clusters/list"
                ]
            }
        elif node_id.startswith("multi"):
            return {
                "k8s": [
                    "kubectl get nodes",
                    "kubectl describe node problem-node"
                ],
                "databricks": [
                    "databricks clusters list",
                    "databricks jobs list"
                ]
            }
        else:
            # Default case
            return {
                "k8s": [
                    "kubectl get nodes --all-namespaces",
                    "systemctl status kubelet"
                ]
            }
    
    def get_triage_steps(self, node_id: str) -> Dict[str, List[str]]:
        """Get triage steps for a specific node."""
        if self.use_mock:
            # Mock triage steps
            return {
                "k8s": [
                    "kubectl get nodes -n default",
                    "kubectl get node " + node_id,
                    "kubectl logs -n default -l app=nginx"
                ],
                "databricks": [
                    "databricks clusters list",
                    "databricks clusters get " + node_id,
                    "databricks jobs list"
                ],
            }
        else:
            # Real implementation would go here
            raise NotImplementedError("Real implementation not available")

    async def get_triage_steps_async(self, node_id: str) -> Dict[str, List[str]]:
        """
        Fetch triage steps from Databricks for a specific node.
        If use_mock is True, returns mock data instead of making actual API calls.
        
        Args:
            node_id: The ID of the node requiring triage
            
        Returns:
            Dict containing platform-specific triage steps
        """
        try:
            if self.use_mock:
                logger.info("Using mock Databricks client")
                triage_steps = await self._get_mock_triage_steps(node_id)
            else:
                # Real implementation
                response = await self.client.jobs.run_now(
                    job_id=os.getenv("TRIAGE_JOB_ID"),
                    parameters={
                        "node_id": node_id
                    }
                )
                
                run_id = response["run_id"]
                
                run_result = await self.client.jobs.get_run_output(
                    run_id=run_id
                )
                
                triage_steps = run_result.get("notebook_output", {})
            
            # Validate the response structure
            if not isinstance(triage_steps, dict):
                raise ValueError("Invalid triage steps format")
                
            for platform, steps in triage_steps.items():
                if not isinstance(steps, list):
                    raise ValueError(f"Invalid steps format for platform {platform}")
                    
            logger.info("Successfully fetched triage steps", 
                       extra={
                           "node_id": node_id,
                           "steps": triage_steps,
                           "mode": "mock" if self.use_mock else "real"
                       })
            
            return triage_steps
            
        except Exception as e:
            logger.error(f"Error fetching triage steps: {str(e)}", 
                        extra={"node_id": node_id})
            raise 