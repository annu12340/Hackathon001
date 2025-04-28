import asyncio
import json
import subprocess
import logging
from typing import Dict, List, Tuple
from . import config

logger = logging.getLogger(__name__)

class TriageService:
    def __init__(self):
        self.command_timeout = config.COMMAND_TIMEOUT
        self.allowed_commands = config.ALLOWED_COMMANDS

    async def _execute_command(self, command: str) -> Tuple[bool, str, str]:
        """Execute a shell command with timeout."""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.command_timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return False, "", f"Command timed out after {self.command_timeout} seconds"
            
            stdout_str = stdout.decode('utf-8').strip()
            stderr_str = stderr.decode('utf-8').strip()
            
            return process.returncode == 0, stdout_str, stderr_str
            
        except Exception as e:
            return False, "", str(e)


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
            
            # response = await self.openai_client.chat.completions.create(
            #     model="gpt-4",
            #     messages=[{"role": "user", "content": prompt}],
            #     temperature=0.2
            # )   
            mock_response = {
                "choices": [{
                    "message": {
                        "content": """{
                            "risk_assessment": {
                                "step1": {"risk": "low", "impact": "minimal"},
                                "step2": {"risk": "medium", "impact": "moderate"},
                                "step3": {"risk": "low", "impact": "minimal"}
                            }
                        }"""
                    }
                }]
            }
            analysis = json.loads(mock_response["choices"][0]["message"]["content"])
            logger.info(f"Step analysis completed for {platform} with analysis: {analysis}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing steps: {str(e)}")
            raise
    
    async def execute_triage_step(self, platform: str, step: str) -> Dict:
        """Execute a single triage step with safety checks."""
        try:
 
            # Analyze the step before execution
            analysis = await self.analyze_triage_steps(platform, [step])
            
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
    
    async def orchestrate_triage(self, triage_data) -> Dict:
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