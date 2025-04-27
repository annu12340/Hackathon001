import os
#import openai

class AzureOpenAIClient:
    def __init__(self):
        # openai.api_type = "azure"
        # openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
        # openai.api_version = "2023-05-15"
        # openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT") 

    def summarize_pagerduty_alert(self, incident):
        # PAGERDUTY_INCIDENT_SUMMARY_PROMPT="""
        #     As an expert incident analyst, your task is to process a PagerDuty alert provided in JSON format. Extract and summarize the key points

        #     **Extraction and Analysis:**

        #     Given the PagerDuty alert JSON, parse and fill in the following core fields:

        #     * **Status:** (Choose from: Acknowledged / Triggered / Resolved)
        #     * **Urgency:** (Choose from: High / Low)
        #     * **Title:** (Directly from the alert title)
        #     * **Summary of the Issue:** (A concise 1-2 sentence human-readable explanation based on the alert description)

        #     Furthermore, analyze the alert 'title' and 'description' to infer and extract the following contextual details:
        #     * **Environment:** (e.g., Kubernetes, Slurm, Cloud, On prem based on keywords)
        #     * **Cluster:** (e.g., lima-rancher-desktop, based on keywords)
        #     * **Node Name:** (eg: Hostname, server, or node affected)
        #     * **Error Type:** (e.g., IOException, MemoryError, DiskFull, based on error logs)
        #     * **Impacted Component:** (Specific filesystem, directory, database, API, etc.)
        #     * **Time:** (UTC time of the incident)    

        #     **Output Report Format:**
        #     Return the output in a json of 1 level, without any nested structure
        # """
        # full_prompt = PAGERDUTY_INCIDENT_SUMMARY_PROMPT + "\nIncident JSON:\n" + str(incident)
        # response = openai.ChatCompletion.create(
        #     engine=self.deployment,
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": full_prompt}
        #     ],
        #     temperature=0.2,
        #     max_tokens=512,
        # )
        # summary = response["choices"][0]["message"]["content"]
        summary={
  "Status": "Acknowledged",
  "Urgency": "High",
  "Title": "Unable to write to temporary directory",
  "Time_UTC": "2025-04-27 04:35:54",
  "Summary_of_the_Issue": "The system encountered an issue where it was unable to write to a temporary directory, which may indicate a permissions issue or lack of available space.",
  "Environment_or_Cluster": "Production (inferred based on urgency)",
  "Host_or_Node_Name": "Not specified",
  "Error_Type": "Filesystem access issue (possible permissions or disk space)",
  "Impacted_Component": "Temporary directory"
}

        return summary