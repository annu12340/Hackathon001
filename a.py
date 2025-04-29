import os
import requests
import pandas as pd
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import subprocess

def execute_action(action):
    try:
        print(f"Executing: {action}")
        # Option 1: Use subprocess if it's a shell command
        result = subprocess.run(action, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr.decode()}")


def create_request_data(message):
    return {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "context": {
            "conversation_id": "test_conversation",
            "user_id": "test_user"
        }
    }

def score_model(message):
    url = 'https://nvidia-edsp-or1.cloud.databricks.com/serving-endpoints/agents_edsp-dgxc-sre-dev-srecet/invocations'
    headers = {
        'Authorization': 'Bearer dapi5e2d077e7e718f2334a6c9d4a955b07b',
        'Content-Type': 'application/json'
    }
    
    # Create the request data with the correct schema
    data = create_request_data(message)
    data_json = json.dumps(data)
    
    response = requests.request(method='POST', headers=headers, url=url, data=data_json)
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()

def test_api():
    # Test cases
    test_messages = [
        """
        PagerDuty: Status: Acknowledged
        Urgency: High
        Title: Unable to write to temporary directory
        Time (UTC): 2025-04-27 04:35:54
        Summary of the Issue: The system encountered an issue where it was unable to write to a temporary directory, which may indicate a permissions issue or lack of available space.
        Environment/Cluster: Production (inferred based on urgency)
        Host/Node Name: Not specified
        Error Type: Filesystem access issue (possible permissions or disk space)
        Impacted Component: Temporary directory
        Time: N/A
        """
    ]
    
    print("Starting API tests...\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}:")
        print(f"Input: {message}")
        
        try:
            # Make API call with the correct schema
            print("Making API call...")
            response = score_model(message)
            
            # Print response
            print("Response received:")
            # result=json.loads(response)
            raw_string=response['messages'][0]['content']
            json_string = raw_string.strip("`json\n").rstrip("`")

            # Step 2: Parse the JSON
            parsed_data = json.loads(json_string)

            # Access individual parts
            print("Summary:", parsed_data["summary"])
            print("Actions:")
            for action in parsed_data["actions"]:
                print("-", action)

            execute_action(parsed_data["actions"][0])
            
            # print(json.dumps(response, indent=2))
            print("\n" + "-"*50 + "\n")
            
        except Exception as e:
            print(f"Error in test {i}: {str(e)}")
            print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
        test_api() 