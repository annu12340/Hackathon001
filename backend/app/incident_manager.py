import logging
import asyncio
import re
from datetime import datetime
from .file_manager import FileManager
from .azure.databricks_client import DatabricksTriageClient
from .utils.pagerduty_client import PagerDutyClient
from .azure.azure_openai import AzureOpenAIClient

logger = logging.getLogger(__name__)

class IncidentManager:
    def __init__(self, app, config):
        self.app = app
        self.pd_client = PagerDutyClient(config.PAGERDUTY_API_KEY)
        self.azure_openai = AzureOpenAIClient()
        self.databricks_client = DatabricksTriageClient()
        self.file_manager = FileManager()

    def extract_incident_id(self, text):
        """Extract a PagerDuty incident ID from alert text"""
        url_pattern = r'pagerduty\.com/incidents/([A-Z0-9]+)'
        url_match = re.search(url_pattern, text)
        if url_match:
            return url_match.group(1)
            
        id_pattern = r'(?:incident\s+#?)([A-Z0-9]{6,})'
        text_match = re.search(id_pattern, text, re.IGNORECASE)
        if text_match:
            return text_match.group(1)
            
        return None

    async def update_status(self, channel, ts, steps_done, current_step, thread_ts):
        """Update the status message with a progress bar and step descriptions."""
        steps = [
            "Getting PagerDuty Alert Info",
            "Analyzing Alert",
            "Fetching Logs",
            "Analyzing Root Cause",
            "Getting Remediation Steps",
            "Running Diagnostics"
        ]
        
        # Create progress bar (8 blocks total)
        progress_blocks = 8
        filled_blocks = int((steps_done / len(steps)) * progress_blocks)
        progress_bar = "█" * filled_blocks + "░" * (progress_blocks - filled_blocks)
        
        # Build the status message
        status_message = [
            f"*Progress: {progress_bar}*",
            f"*{int((steps_done / len(steps)) * 100)}% Complete*\n"
        ]
        
        # Add step statuses
        for i, step in enumerate(steps):
            if i+1 < steps_done or current_step=="Running Diagnostics":
                status = "✅"
            elif i+1 == steps_done:
                status = ":loading-dot:"
            else:
                status = ":white_small_square:"
            status_message.append(f"{status} {step}\n")
        
        # Add current step information
        status_message.append(f"*Current Step:* {current_step} \n")
        
        await self.app.client.chat_update(
            channel=channel,
            ts=ts,
            text="\n".join(status_message),
            thread_ts=thread_ts
        )


    async def handle_alert(self, text: str, thread_ts: str, say):
        """Handle all alerts including PagerDuty incidents"""
        try:
            # Send initial processing message
            await say(text=":hourglass_flowing_sand: *Starting the analysis...*", thread_ts=thread_ts)
            initial_message = await say(text=".", thread_ts=thread_ts)
            message_ts = initial_message['ts']
            channel = initial_message['channel']
            
            # Step 1: Check if this is a PagerDuty incident and get details if it is
            await self.update_status(channel, message_ts, steps_done=1, 
                                       current_step="Getting pagerduty alert info", 
                                       thread_ts=thread_ts)
            incident_id = "Q3TAMBYDY6HQI4"  # This should be extracted from text
            if incident_id:
                logger.info(f"Found PagerDuty incident ID: {incident_id}")
                # incident_dic = self.pd_client.get_incident(incident_id)

            # if incident_dic:
            #     await self.update_status(channel, message_ts, steps_done=2, 
            #                        current_step="Analyzing alert", 
            #                        thread_ts=thread_ts)
            #     summary = self.azure_openai.summarize_pagerduty_alert(incident_dic)
            #     summarized_pd_alert = self.pd_client.format_incident_details(summary)
            #     print("detailed message is", summarized_pd_alert)
            # else:
            #     return
            summarized_pd_alert = {
    "Status": "Acknowledged",
    "Urgency": "High",
    "Title": "Unable to write to temporary directory",
    "Time_UTC": "2025-04-27 04:35:54",
    "Summary": "The system encountered an issue where it was unable to write to a temporary directory, which may indicate a permissions issue or lack of available space.",
    "Environment_Cluster": "Production (inferred based on urgency)",
    "Host_Node_Name": "Not specified",
    "Error_Type": "Filesystem access issue (possible permissions or disk space)",
    "Impacted_Component": "Temporary directory",
    "Reported_Time": "N/A"
}

            # await self.update_status(channel, message_ts, steps_done=3, 
            #                        current_step="Fetching the appropriate logs", 
            #                        thread_ts=thread_ts)
            # log_result=self.databricks_client.get_and_analyze_logs(cluster,node_id,summary.get("platform"))
            # await asyncio.sleep(2)
            
            # await self.update_status(channel, message_ts, steps_done=4, 
            #                        current_step="Analyzing root cause", 
            #                        thread_ts=thread_ts)
            cluster="lima-rancher-desktop"
            node_id = "lima-rancher-desktop"
            incident_dic={}
            triage_steps={
  "summary": "The system is unable to write to a temporary directory, which may indicate a permissions issue or lack of available space. Check the permissions of the temporary directory and ensure that there is sufficient available space.",
  "actions": [
    {"command":"df -h", "risk":"low"},
    {"command":"ls -ld /tmp", "risk":"high"},
  ]
}
            # await self.update_status(channel, message_ts, steps_done=5, 
            #                        current_step="Getting the remediation steps", 
            #                        thread_ts=thread_ts)
            # triage_steps = self.databricks_client.get_triage_steps(cluster,node_id,summarized_pd_alert,log_result)
            # await asyncio.sleep(2)

            await self.update_status(channel, message_ts, steps_done=6, 
                                   current_step="Running diagnostics", 
                                   thread_ts=thread_ts)
            
            results =  await self.databricks_client.orchestrate_triage(cluster,node_id,triage_steps,say,thread_ts)
            await asyncio.sleep(2)
            
            # await self.file_manager.update_incident_files(incident_id, incident_dic, results)
            
            detailed_analysis_url = f"http://localhost:3000/{incident_id}"
            final_message = f"""
                \n\n\n\n*Analysis Complete:sparkles:!* 
                \n📊 <{detailed_analysis_url}|View detailed analysis>
            """
            await say(text=final_message, thread_ts=thread_ts)

        except Exception as e:
            logger.exception(f"Error handling alert: {str(e)}")
            if 'message_ts' in locals() and 'channel' in locals():
                await self.app.client.chat_update(
                    channel=channel,
                    ts=message_ts,
                    text=f":x: Error: {str(e)}",
                    thread_ts=thread_ts
                )
            else:
                await say(text=f":x: Error: {str(e)}", thread_ts=thread_ts)