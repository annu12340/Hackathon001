import asyncio
from typing import Dict, Tuple
from datetime import datetime

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

    async def execute_rdctl_command(self, command: str) -> Tuple[bool, str, str]:
        """Execute a command using rdctl shell."""
        try:
            rdctl_command = f"rdctl shell {command}"
            print(f"Executing rdctl command: {command}")
            
            process = await asyncio.create_subprocess_shell(
                rdctl_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            success = process.returncode == 0
            
            if not success:
                print(f"rdctl command failed: {stderr.decode('utf-8')}")
            
            return success, stdout.decode('utf-8'), stderr.decode('utf-8')
            
        except Exception as e:
            print(f"Error executing rdctl command: {e}")
            return False, "", str(e)

    async def execute_ssh_command(self, host: str, command: str) -> Tuple[bool, str, str]:
        """Fallback method to execute command via SSH."""
        try:
            ssh_command = (
                f"ssh -i {self.ssh_key_path} -o StrictHostKeyChecking=no "
                f"-o ConnectTimeout=10 {host} '{command}'"
            )
            
            print(f"Executing SSH command on {host}: {command}")
            
            process = await asyncio.create_subprocess_shell(
                ssh_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            success = process.returncode == 0
            
            return success, stdout.decode('utf-8'), stderr.decode('utf-8')
            
        except Exception as e:
            print(f"SSH command failed for {host}: {e}")
            return False, "", str(e)

    async def execute_command(self, host: str, command: str, use_rdctl: bool = True) -> Tuple[bool, str, str]:
        """Execute command using rdctl or fallback to SSH."""
        if use_rdctl:
            success, stdout, stderr = await self.execute_rdctl_command(command)
            if success or "rdctl" not in stderr:
                return success, stdout, stderr
            
            print(f"rdctl failed, falling back to SSH for {host}")
        
        return await self.execute_ssh_command(host, command)

    async def collect_system_info(self, host: str, use_rdctl: bool = True) -> Dict[str, str]:
        """Collect basic system information."""
        print(f"Collecting system information from {host}")
        
        commands = {
            "uname": "uname -a",
            "uptime": "uptime",
            "memory": "free -m",
            "disk": "df -h",
            "cpu": "top -bn1 | head -n 5",
            "processes": "ps aux | sort -rk 3,3 | head -n 10",
            "network": "netstat -tuln",
            "docker_status": "systemctl status docker",
            "kubelet_status": "systemctl status kubelet",
            "rancher_status": "rdctl version"
        }
        
        system_info = {}
        for key, cmd in commands.items():
            print(f"Collecting {key} information...")
            success, stdout, stderr = await self.execute_command(host, cmd, use_rdctl)
            system_info[key] = stdout if success else f"Error: {stderr}"
            
        return system_info

    async def collect_recent_logs(self, host: str, lines: int = 100, use_rdctl: bool = True) -> Dict[str, str]:
        """Collect recent logs from important log files."""
        print(f"Collecting recent logs from {host}")
        
        logs = {}
        
        for log_file in self.important_logs:
            print(f"Checking log file: {log_file}")
            
            check_cmd = f"test -f {log_file} && echo 'exists' || echo 'not found'"
            success, stdout, _ = await self.execute_command(host, check_cmd, use_rdctl)
            
            if success and 'exists' in stdout:
                print(f"Collecting content from {log_file}")
                cmd = f"tail -n {lines} {log_file}"
                success, stdout, stderr = await self.execute_command(host, cmd, use_rdctl)
                if success:
                    logs[log_file] = stdout
                else:
                    print(f"Failed to collect logs from {log_file}: {stderr}")
        
        # Add Rancher Desktop specific logs
        rd_logs = [
            "rdctl logs",
            "rdctl shell -- journalctl -u kubelet --no-pager -n 100",
            "rdctl shell -- docker logs --tail 100"
        ]
        
        for cmd in rd_logs:
            print(f"Collecting Rancher Desktop logs: {cmd}")
            success, stdout, stderr = await self.execute_command(host, cmd, use_rdctl=True)
            if success:
                logs[cmd] = stdout
        
        return logs

    async def collect_all_diagnostics(self, host: str, use_rdctl: bool = True) -> Dict[str, Dict]:
        """Collect all diagnostic information from the node."""
        print(f"\nStarting diagnostic collection for {host}")
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Check if rdctl is available
            if use_rdctl:
                _, _, stderr = await self.execute_rdctl_command("version")
                use_rdctl = "rdctl" not in stderr
                
                if not use_rdctl:
                    print("rdctl not available, falling back to SSH")
            
            print("Collecting diagnostics...")
            system_info, logs = await asyncio.gather(
                self.collect_system_info(host, use_rdctl),
                self.collect_recent_logs(host, use_rdctl=use_rdctl)
            )
            
            diagnostics = {
                "timestamp": timestamp,
                "host": host,
                "system_info": system_info,
                "logs": logs,
                "collection_method": "rdctl" if use_rdctl else "ssh"
            }
            
            print(f"Diagnostic collection complete using {diagnostics['collection_method']}")
            print(f"Collected {len(system_info)} system metrics and {len(logs)} log files")
            
            return diagnostics
            
        except Exception as e:
            print(f"Error collecting diagnostics: {e}")
            return {
                "timestamp": timestamp,
                "host": host,
                "error": str(e)
            }

    def format_diagnostics_report(self, diagnostics: Dict) -> str:
        """Format diagnostics information into a readable report."""
        print("Formatting diagnostic report...")
        sections = []
        
        # Header
        sections.append(f"Diagnostics Report for {diagnostics['host']}")
        sections.append(f"Generated at: {diagnostics['timestamp']}\n")
        
        # System Information
        sections.append("=== System Information ===")
        for key, value in diagnostics.get('system_info', {}).items():
            sections.append(f"\n--- {key.upper()} ---")
            sections.append(value)
        
        # Important Logs
        sections.append("\n=== Recent Logs ===")
        for log_file, content in diagnostics.get('logs', {}).items():
            sections.append(f"\n--- {log_file} ---")
            sections.append(content[:1000] + "..." if len(content) > 1000 else content)
        
        print("Report formatting complete")
        return "\n".join(sections) 