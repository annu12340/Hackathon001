import logging
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class FileManager:
    async def update_incident_files(self, incident_id, incident_dic, results):
        """Update JSON files for the incident"""
        logger.info(f"Updating incident files for {incident_id}")
        try:
            # Create directory structure
            base_dir = os.path.join(os.getcwd(), "frontend", "public", "data")
            incident_dir = os.path.join(base_dir, incident_id)
            os.makedirs(incident_dir, exist_ok=True)

            # Generate data.json
            data = {
                "overview": {
                    "title": f"{incident_dic.get('service', {}).get('name', 'Service')} Incident Dashboard",
                    "alertDetails": {
                        "status": incident_dic.get('status', 'unknown').upper(),
                        "urgency": incident_dic.get('urgency', 'unknown').upper(),
                        "title": incident_dic.get('title', 'Unknown Incident'),
                        "service": incident_dic.get('service', {}).get('name', 'Unknown Service'),
                        "created": incident_dic.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")),
                        "lastUpdated": incident_dic.get('last_status_change_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")),
                        "assignedTo": incident_dic.get('assignments', [{}])[0].get('assignee', {}).get('name', 'Unassigned')
                    },
                    "aiGeneratedData": {
                        "alertSummary": incident_dic.get('description', 'No description available'),
                        "confidence": "High",
                        "environment": "Production",
                        "cluster": incident_dic.get('service', {}).get('name', 'Unknown Cluster'),
                        "nodeName": incident_dic.get('service', {}).get('name', 'Unknown Node'),
                        "errorType": incident_dic.get('type', 'Unknown Error'),
                        "errorSeverity": incident_dic.get('urgency', 'Unknown').capitalize(),
                        "impactedComponent": incident_dic.get('service', {}).get('name', 'Unknown Component'),
                        "componentVersion": "v2.3.1",
                        "firstDetected": incident_dic.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))
                    }
                },
                "logs": {
                    "logSummaryStats": [
                        {"label": "Errors", "value": len([l for l in results.get('logs', []) if l.get('level') == 'ERROR']), "delta": 0},
                        {"label": "Warnings", "value": len([l for l in results.get('logs', []) if l.get('level') == 'WARN']), "delta": 0},
                        {"label": "Info", "value": len([l for l in results.get('logs', []) if l.get('level') == 'INFO']), "delta": 0}
                    ],
                    "logData": {
                        "kubectl": results.get('logs', [])
                    }
                },
                "followUpTasks": [
                    {
                        "id": 1,
                        "title": f"Review {incident_dic.get('service', {}).get('name', 'service')} after fix implementation",
                        "dueDate": (datetime.now()).strftime("%Y-%m-%d"),
                        "priority": "high" if incident_dic.get('urgency') == 'high' else "medium",
                        "completed": False,
                        "assignee": incident_dic.get('assignments', [{}])[0].get('assignee', {}).get('name', 'Unassigned')
                    },
                ],
            }

            # Write data.json
            with open(os.path.join(incident_dir, "data.json"), "w") as f:
                json.dump(data, f, indent=2)

            # Generate remediation steps
            remediation_steps = []
            for platform, platform_data in results.items():
                for step in platform_data.get('steps_results', []):
                    remediation_steps.append({
                        "id": str(len(remediation_steps) + 1),
                        "title": step.get('step', 'Unknown Step'),
                        "description": step.get('message', 'No description available'),
                        "status": step.get('status', 'pending')
                    })

            # Write remediationSteps.json
            with open(os.path.join(incident_dir, "remediationSteps.json"), "w") as f:
                json.dump({"remediationSteps": remediation_steps}, f, indent=2)

            logger.info(f"Updated incident files for {incident_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating incident files: {str(e)}")
            return False 