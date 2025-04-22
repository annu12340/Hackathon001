import asyncio
import subprocess
import logging
from typing import Dict, List, Tuple
from . import config

logger = logging.getLogger(__name__)

class TriageService:
    def __init__(self):
        self.command_timeout = config.COMMAND_TIMEOUT
        self.allowed_commands = config.ALLOWED_COMMANDS

    async def execute_command(self, command: str) -> Tuple[bool, str, str]:
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

    def is_command_allowed(self, platform: str, command: str) -> bool:
        """Check if command is allowed for the given platform."""
        if platform not in self.allowed_commands:
            return False
        return any(command.startswith(cmd) for cmd in self.allowed_commands[platform])

    async def execute_triage_step(self, platform: str, step: str) -> Dict:
        """Execute a single triage step."""
        if not self.is_command_allowed(platform, step):
            return {
                "status": "error",
                "message": "Command not allowed",
                "step": step
            }

        success, output, error = await self.execute_command(step)
        
        if success:
            return {
                "status": "success",
                "step": step,
                "output": output
            }
        else:
            return {
                "status": "error",
                "message": error or "Command failed",
                "step": step,
                "output": output
            }

    async def orchestrate_triage(self, triage_data: Dict[str, List[str]]) -> Dict:
        """Run all triage steps for each platform."""
        results = {}
        
        for platform, steps in triage_data.items():
            platform_results = []
            
            for step in steps:
                result = await self.execute_triage_step(platform, step)
                platform_results.append(result)
                
                if result["status"] == "error":
                    break
                    
            results[platform] = platform_results
            
        return results 