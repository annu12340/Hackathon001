import os
import json
import logging
import asyncio
import subprocess
from typing import Dict, List, Tuple
import openai
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pythonjsonlogger import jsonlogger

# Configure logging
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

class TriageAgent:
    def __init__(self):
        # Initialize Azure OpenAI client
        self.credential = DefaultAzureCredential()
        self.openai_client = openai.AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview"
        )
        
        # Safety configurations
        self.ALLOWED_COMMANDS = {
            "k8s": ["systemctl", "kubectl", "journalctl"],
            "databricks": ["databricks", "curl"]
        }
        
        # Command timeout in seconds
        self.COMMAND_TIMEOUT = 300  # 5 minutes default timeout
        
    async def _execute_command(self, command: str) -> Tuple[bool, str, str]:
        """
        Execute a shell command asynchronously with timeout.
        
        Args:
            command: The command to execute
            
        Returns:
            Tuple of (success, output, error)
        """
        try:
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for the process with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.COMMAND_TIMEOUT
                )
            except asyncio.TimeoutError:
                # Kill the process if it times out
                process.kill()
                return False, "", f"Command timed out after {self.COMMAND_TIMEOUT} seconds"
            
            # Decode output
            stdout_str = stdout.decode('utf-8').strip()
            stderr_str = stderr.decode('utf-8').strip()
            
            # Check return code
            success = process.returncode == 0
            
            return success, stdout_str, stderr_str
            
        except Exception as e:
            return False, "", str(e)
    
    async def validate_commands(self, platform: str, commands: List[str]) -> bool:
        """Validate if the commands are safe to execute."""
        if platform not in self.ALLOWED_COMMANDS:
            logger.warning(f"Unsupported platform: {platform}")
            return False
            
        allowed = self.ALLOWED_COMMANDS[platform]
        for cmd in commands:
            if not any(cmd.startswith(safe_cmd) for safe_cmd in allowed):
                logger.warning(f"Potentially unsafe command detected: {cmd}")
                return False
        return True
    
    async def analyze_triage_steps(self, platform: str, steps: List[str]) -> Dict:
        """Analyze triage steps using Azure OpenAI."""
        try:
            prompt = f"""
            Analyze the following triage steps for {platform} platform:
            {json.dumps(steps)}
            
            Provide:
            1. Risk assessment for each step
            2. Expected outcome
            3. Potential failure scenarios
            4. Recovery steps if something goes wrong
            
            Format the response as JSON.
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            analysis = json.loads(response.choices[0].message.content)
            logger.info(f"Step analysis completed for {platform}", extra={"analysis": analysis})
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing steps: {str(e)}")
            raise
    
    async def execute_triage_step(self, platform: str, step: str) -> Dict:
        """Execute a single triage step with safety checks."""
        try:
            # Validate the command
            if not await self.validate_commands(platform, [step]):
                return {
                    "status": "error",
                    "message": "Command validation failed",
                    "step": step
                }
            
            # Analyze the step before execution
            analysis = await self.analyze_triage_steps(platform, [step])
            
            # If risk is too high, require manual approval
            if analysis.get("risk_level", "low") == "high":
                return {
                    "status": "pending_approval",
                    "message": "High-risk command requires manual approval",
                    "step": step,
                    "analysis": analysis
                }
            
            # Execute the command
            logger.info(f"Executing step: {step}")
            success, output, error = await self._execute_command(step)
            
            if success:
                return {
                    "status": "success",
                    "message": "Step executed successfully",
                    "step": step,
                    "output": output,
                    "analysis": analysis
                }
            else:
                error_msg = error if error else "Command failed with no error message"
                logger.error(f"Command execution failed: {error_msg}")
                return {
                    "status": "error",
                    "message": error_msg,
                    "step": step,
                    "output": output,
                    "error": error,
                    "analysis": analysis
                }
            
        except Exception as e:
            logger.error(f"Error executing step: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "step": step
            }
    
    async def orchestrate_triage(self, triage_data: Dict[str, List[str]]) -> Dict:
        """Orchestrate the entire triage process."""
        results = {}
        
        for platform, steps in triage_data.items():
            platform_results = []
            
            # Analyze all steps first
            analysis = await self.analyze_triage_steps(platform, steps)
            
            # Execute steps sequentially
            for step in steps:
                result = await self.execute_triage_step(platform, step)
                platform_results.append(result)
                
                # If a step fails, stop execution for this platform
                if result["status"] == "error":
                    logger.error(f"Stopping execution for {platform} due to error")
                    break
                    
            results[platform] = {
                "steps_results": platform_results,
                "analysis": analysis
            }
            
        return results 