import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class LogCollector:
    def __init__(self, ssh_key_path: str = "~/.ssh/id_rsa"):
        self.ssh_key_path = ssh_key_path
        self.important_logs = [
            "/var/log/syslog",
            "/var/log/kern.log",
            "/var/log/auth.log",
            "/var/log/dmesg",
            "/var/log/kubernetes/kubelet.log",
            "/var/log/containers/*",
            "/var/log/pods/*"
        ]
        
    async def execute_ssh_command(self, host: str, command: str) -> tuple[bool, str, str]:
        """Execute a command over SSH using asyncio subprocess."""
        try:
            ssh_command = (
                f"ssh -i {self.ssh_key_path} -o StrictHostKeyChecking=no "
                f"-o ConnectTimeout=10 {host} '{command}'"
            )
            
            process = await asyncio.create_subprocess_shell(
                ssh_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            success = process.returncode == 0
            
            return success, stdout.decode('utf-8'), stderr.decode('utf-8')
            
        except Exception as e:
            logger.error(f"SSH command execution failed: {e}")
            return False, "", str(e)

    async def collect_system_info(self, host: str) -> Dict[str, str]:
        """Collect basic system information."""
        commands = {
            "uname": "uname -a",
            "uptime": "uptime",
            "memory": "free -m",
            "disk": "df -h",
            "cpu": "top -bn1 | head -n 5",
            "processes": "ps aux | sort -rk 3,3 | head -n 10",
            "network": "netstat -tuln",
            "docker_status": "systemctl status docker",
            "kubelet_status": "systemctl status kubelet"
        }
        
        system_info = {}
        for key, cmd in commands.items():
            success, stdout, stderr = await self.execute_ssh_command(host,  cmd)
            system_info[key] = stdout if success else f"Error: {stderr}"
            
        return system_info

    async def collect_recent_logs(self, host: str, user: str, lines: int = 100) -> Dict[str, str]:
        """Collect recent logs from important log files."""
        logs = {}
        
        for log_file in self.important_logs:
            # First check if file exists
            check_cmd = f"test -f {log_file} && echo 'exists' || echo 'not found'"
            success, stdout, _ = await self.execute_ssh_command(host,  check_cmd)
            
            if success and 'exists' in stdout:
                # Collect recent logs with timestamp
                cmd = f"tail -n {lines} {log_file}"
                success, stdout, stderr = await self.execute_ssh_command(host,  cmd)
                if success:
                    logs[log_file] = stdout
        
        return logs


    async def collect_all_diagnostics(self, host: str) -> Dict[str, Dict]:
        """Collect all diagnostic information from the node."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Collect all information concurrently
            system_info, logs, k8s_info = await asyncio.gather(
                self.collect_system_info(host),
                self.collect_recent_logs(host),
            )
            
            diagnostics = {
                "timestamp": timestamp,
                "host": host,
                "system_info": system_info,
                "logs": logs,
                "kubernetes_info": k8s_info
            }
            
            return diagnostics
            
        except Exception as e:
            logger.error(f"Error collecting diagnostics: {e}")
            return {
                "timestamp": timestamp,
                "host": host,
                "error": str(e)
            }

    def format_diagnostics_report(self, diagnostics: Dict) -> str:
        """Format diagnostics information into a readable report."""
        sections = []
        
        # Header
        sections.append(f"Diagnostics Report for {diagnostics['host']}")
        sections.append(f"Generated at: {diagnostics['timestamp']}\n")
        
        # System Information
        sections.append("=== System Information ===")
        for key, value in diagnostics.get('system_info', {}).items():
            sections.append(f"\n--- {key.upper()} ---")
            sections.append(value)
        
        # Kubernetes Information
        sections.append("\n=== Kubernetes Information ===")
        for key, value in diagnostics.get('kubernetes_info', {}).items():
            sections.append(f"\n--- {key.upper()} ---")
            sections.append(value)
        
        # Important Logs
        sections.append("\n=== Recent Logs ===")
        for log_file, content in diagnostics.get('logs', {}).items():
            sections.append(f"\n--- {log_file} ---")
            sections.append(content[:1000] + "..." if len(content) > 1000 else content)
        
        return "\n".join(sections) 