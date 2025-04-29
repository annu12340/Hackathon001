import os
from openai import AzureOpenAI

class AzureOpenAIClient:
    def __init__(self):
        self.api_version = "2023-07-01-preview"
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENxT")

    def summarize_pagerduty_alert(self, incident):
        PAGERDUTY_INCIDENT_SUMMARY_PROMPT = """
            As an expert incident analyst, your task is to process a PagerDuty alert provided in JSON format. Extract and summarize the key points

            **Extraction and Analysis:**

            Given the PagerDuty alert JSON, parse and fill in the following core fields:

            * **Status:** (Choose from: Acknowledged / Triggered / Resolved)
            * **Urgency:** (Choose from: High / Low)
            * **Title:** (Directly from the alert title)
            * **Summary of the Issue:** (A concise 1-2 sentence human-readable explanation based on the alert description)

            Furthermore, analyze the alert 'title' and 'description' to infer and extract the following contextual details:
            * **Environment:** (e.g., Kubernetes, Slurm, Cloud, On prem based on keywords)
            * **Cluster:** (e.g., lima-rancher-desktop, based on keywords)
            * **Node Name:** (eg: Hostname, server, or node affected)
            * **Error Type:** (e.g., IOException, MemoryError, DiskFull, based on error logs)
            * **Impacted Component:** (Specific filesystem, directory, database, API, etc.)
            * **Time:** (UTC time of the incident)    

            **Output Report Format:**
            Return the output in a json of 1 level, without any nested structure
        """
        full_prompt = PAGERDUTY_INCIDENT_SUMMARY_PROMPT + "\nIncident JSON:\n" + str(incident)
        
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2,
            max_tokens=512
        )

        return completion.choices[0].message.content
a=AzureOpenAIClient()
b=a.summarize_pagerduty_alert({"title":"test","description":"test"})
print(b)