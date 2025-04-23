Flow of events

```
Start
  ↓
Initialize Bot
  ↓
  ├── Load Slack Bot Token
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
```