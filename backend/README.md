Flow of events

```
Start
  ↓
Initialize Bot
  ↓
  ├── Load Slack Bot Token
  ├── Load PagerDuty API Key
  └── Initialize RunbookSearch
  ↓
Wait for Messages
  ↓
Message Received
  ↓
  ├── Is it from a bot? → Yes → Ignore
  └── No → Continue
  ↓
Extract Message Info
  ↓
  ├── Text
  ├── Channel
  └── Thread ID
  ↓
Check for "PagerDuty"
  ↓
  ├── Not Found → End
  └── Found → Continue
      ↓
      Is it a PagerDuty incident?
      ↓
      ├── Yes → Extract Incident ID
      │      ↓
      │      Call PagerDuty API
      │      ↓
      │      ├── Success → Display Incident Details
      │      └── Failure → Show Error
      │      ↓
      │      Continue with Triage (optional)
      │
      └── No → Continue with standard triage
          ↓
          Search Runbooks
          ↓
          ├── Remove "PagerDuty:" prefix
          ├── Convert to lowercase
          └── Search mock data
          ↓
          Check Results
          ↓
          ├── Found → Format and Send Response
          └── Not Found → Send "No Results" Message
  ↓
End

## Environment Setup

To run this application, you need to create a `.env` file with the following variables:

```
# Slack configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token

# PagerDuty configuration
PAGERDUTY_API_KEY=your-pagerduty-api-key
```

## PagerDuty Integration

This bot integrates with PagerDuty to fetch incident details when it detects a PagerDuty alert in Slack. The integration works as follows:

1. When a message containing "PagerDuty" and "incident" is detected in Slack
2. The bot extracts the incident ID from the message
3. It calls the PagerDuty API to fetch incident details
4. The details are formatted and posted in the thread
5. Optionally, standard triage steps are performed after fetching the incident details

### PagerDuty API Usage

The bot uses the PagerDuty REST API v2 to fetch incident details. The key elements of the implementation are:

- Authentication via API token
- Fetching incident data via `/incidents/{id}` endpoint
- Formatting incident details for display in Slack
- Error handling for API failures

For more information on the PagerDuty API, see the [official documentation](https://developer.pagerduty.com/api-reference/).