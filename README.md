# 🚀  Kasper: The AI Incident Commander 

Kasper is an AI-powered incident management system that automates and streamlines the incident response lifecycle.

## Table of Contents
- [📋 Project Overview](#project-overview)
  - [Problem Statement](#problem-statement)
  - [Solution](#solution)
  - [Key Features](#key-features)
- [⚙️ Technical Implementation](#technical-implementation)
  - [Architecture](#architecture)
  - [Tech Stack](#tech-stack)
  - [Flow of Events](#flow-of-events)
  - [AI Agents](#ai-agents)
  - [Why Azure Databricks](#why-azure-databricks)
- [📊 Project Details](#project-details)
  - [Submission Details](#submission-details)
  - [Language & Framework](#language--framework)
  - [Project Repository URL](#project-repository-url)
  - [Project Video](#project-video)
  - [Deployed Endpoint](#deployed-endpoint)
  - [Team Members](#team-members)
- [📈 Impact & Benefits](#impact)
  - [Cost Savings](#cost-savings)
  - [Efficiency Gains](#efficiency-gains)
- [🎯 Judging Criteria](#how-kasper-fits-the-judging-criteria)
  - [Innovation](#innovation)
  - [Impact](#impact-1)
  - [Usability](#usability)
  - [Solution Quality](#solution-quality)
  - [Hackathon Alignment](#alignment-with-hackathon-category)
- [💻 Development](#development)
  - [Code Structure](#code-structure)
  - [Frontend Structure](#frontend-structure)
  - [Backend Structure](#backend-structure)
  - [Key Components](#key-components)
- [🔧 Setup & Configuration](#setup--configuration)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Environment Variables](#environment-variables)
  - [Registration Check](#registration-check)

### Submission details
#### Language & Framework

- [x] Python
- [ ] C#
- [ ] Java
- [x] JavaScript/TypeScript
- [ ] Microsoft Copilot Studio
- [ ] Microsoft 365 Agents SDK
- [x] Azure AI Agent Service

#### Project Repository URL

https://github.com/annu12340/Hackathon001

#### Project Video

[Demo video](https://youtu.be/8RMWyVQAzR8)

#### Deployed endpoint

https://kasper-response.framer.website/

#### Team Members

annu12340, armgp 

Contact email: annujolly@gmail.com, arm.gp23@gmail.com

## 📋 Project Overview

### Problem Statement
Modern IT systems, while incredibly powerful, are also incredibly complex, a labyrinth of interconnected services and dependencies. This complexity translates into a torrential flood of data, making it nearly impossible for human engineers to effectively manage incidents at scale. The problem is multifaceted, a hydra-headed challenge that demands a new approach:

- Alert Fatigue: On-call engineers are bombarded with a relentless barrage of alerts, many of which are false positives, low-priority notifications, or simply noise. This constant bombardment leads to alert fatigue

- Context Scarcity: Alerts often provide minimal context, leaving responders to manually piece together the puzzle from disparate systems, like detectives at a crime scene with only a handful of clues. This "context gap" wastes valuable time, delays effective action, and increases the likelihood of misdiagnosis.

- Manual Diagnostics: Troubleshooting remains a largely manual process, involving tedious tasks like sifting through mountains of log data, performing repetitive system checks, and frantically searching through outdated and often inaccurate runbooks. This is time-consuming, error-prone, and utterly unsustainable in the face of modern IT complexity.

- Delayed Resolution: The combined effect of alert fatigue, context scarcity, and manual diagnostics results in prolonged incident resolution times, increased downtime, and significant business disruption. Every minute of downtime translates to lost revenue, lost productivity, and damaged reputation.


### Solution
Kasper isn't just another monitoring tool; it's your AI-powered incident commander, automating and streamlining the entire incident lifecycle. By integrating seamlessly with alerting platforms like PagerDuty, communication hubs like Slack and the power of azure AI gents, Kasper provides a unified, context-rich, and actionable approach to incident management. 

At its core, Kasper harnesses the power of Large Language Models (LLMs) to transcend mere alerting. It understands the incident's narrative, diagnoses the underlying problem with machine precision, prescribes the optimal solution – significantly reducing MTTR and paving the way for truly resilient systems. 


### Key Features
- Real-time incident detection and analysis
- Automated log processing and summarization
- Intelligent remediation recommendations
- Risk-based action execution
- Human-in-the-loop approval for critical actions
- Comprehensive incident tracking and history


## Flow of Events

![Alt text](https://i.ibb.co/k2LtYHXR/Flow-of-events-visual-selection.png)

1. PagerDuty Alert Trigger: An incident occurs, triggering an alert in PagerDuty.

2. Slack Notification: PagerDuty sends a notification about the new alert to a designated Slack channel.

3. Kasper Bot Detection: Kasper's bot, constantly monitoring the specified Slack channel, detects the new PagerDuty alert notification.

4. Initial Alert Summarization (Azure OpenAI): Upon detection, Kasper extracts the pd id and get the entire PD description. It sends it to Azure OpenAI for a concise summary of the PagerDuty alert details.

5. Relevant Log Retrieval: Based on the incident details (e.g., affected service, hostname), Kasper automatically identifies and retrieves the relevant logs from the involved systems.

6. Large Log Summarization (Azure Databricks):  Kasper utilizes Azure Databricks to efficiently process and summarize the key information and error patterns within the logs.

7. Runbook Retrieval (Vector Database): With the summarized alert and log context, Kasper queries a vector database. This database stores embeddings of runbooks, allowing Kasper to perform a semantic search and retrieve the most relevant remediation steps based on the contextual understanding of the incident. There are various tools deployed in the azure databricks to optimize this search

8. Risk Assessment: Kasper assesses the risk level associated with the retrieved remediation steps (e.g., commands like kubectl get pods is low risk, but commands like rm -rf . is high risk).

9. Automated Execution (Low Risk): If the assessed risk of the recommended command is low, Kasper automatically executes the remediation steps on the affected system.

10. Human Approval Request (High Risk): If the assessed risk is high, Kasper posts the summarized incident details, the proposed remediation steps, and the associated risk level to the Slack channel, awaiting explicit approval from an on-call engineer. Once there is enough confidence, this step also can be automated

11. Execution Upon Approval: Once an engineer reviews and approves the remediation steps in Slack, Kasper proceeds to execute the commands on the affected system.

12. Confirmation and Follow-up: After attempting remediation, Kasper posts a confirmation message in Slack, detailing the actions taken and the outcome. It may also suggest potential follow-up actions  based on the incident.


## ⚙️ Technical Implementation

### Architecture

![Text](https://media-hosting.imagekit.io/445649bdad484c49/diagram-export-30-04-2025-08_46_52.png?Expires=1840600831&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=D~qhF8vNgoXHnd0OEEnhv-O-sfd7eHQ2RH3uiGvIgFFI1dGB82QVwcqahYw9gT12BJnaeWvpd99AeRtSuXCtXUOrvK02vpcG0nU-SMsh3mGuPGgm2V5grSO0kPLMlQi-v5kfNFlY51hOGAnmIi9cXq8MZqlF9iRTCDcbfEzfPPwXkI9Nv4vxqP6ZfK--r8KHaiwsypkt85~QFhqkWD2NK~rdfkNTFiad9bfma~i7-bjW8WisA-SgQFrpgQf3P5KuDZQZPefF1HMV2766SWlc9B5geaN7FHy0s~GWH1vc~XGVVMW-9hR1SIc-1M0VttuuZ5Ri5pwvJsClzFt2gUQCjQ__)

### Tech Stack
- Frontend:
  - React 18
  - TypeScript
  - Vite
  - TailwindCSS
  - Axios for API calls

- Backend:
  - Python 
  - Azure SDKs for service integration

- Microsoft Azure Services:
    - Azure AI Agents using azure Databricks
    - Azure OpenAI
    - Azure Cosmos DB
    - Azure Vector Search

- Integration Services:
    - Slack (for communication)
    - PagerDuty (for incident management)
    - Azure cosmos db

![text](https://media-hosting.imagekit.io/2c23e4a6cadd4fd0/diagram-export-30-04-2025-08_34_01.png?Expires=1840600837&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=qrZkLpL6R0BlBBM6VvdVknJc6gfQvZXd7PIutq50r5iof8Qkus5icQwF8enUtvgLVFR8ZL~wB3uwSWJ1GIiSohqYyzLQWMyXBsI-13XXhGw1daNeE8D4gi3iNCbriPRGwsAyfTl9xXkVdk5rV83x0jW57KobxeeVF7l6QXMw3EDXaPHur12dm7LzCyCMHV20dDC4afy-4UDAf-PmA9VUAdZTtgUDID0QrvgqAUsc-aoRVjj~ZCDaYl3ql~7aItmjCOQdwcs60DSM3ipL4FTcDCvG3av22h~w1B3L4iiPh9uml0rdx9cXlrWt1A5MPHRqUiIBVZnush5SJqmyXcGTQg__)

### AI Agents interact in azure databricks

![test](https://media-hosting.imagekit.io/11db7186ca1c4a70/kasper.jpeg?Expires=1840600767&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=BGJWOBzqTRSiZbErf7KHndp7pN0~oZVWRYhERQBxdb5nbdiYQX54hID~8IZWGpkIfP~Tm03uw7lLvZDdjlvcOUANaIeXCt6NBiC~1JoeCGFatkqQGFxa326VZD2YPU-4nJ71hQ9okO-yIqWVVvM7e3RzO~dzLFjMh9-4kKXvFofxTQDwIz7naHiEjL2qU1jvnYQ3O0eH4CaQvhtuvub-z8IHFL5n7se4~XOALoNOM~C65X0rIRhiBvNwKnZQcz~x2lAkj0q6mgtIxpMvzhDSDupY7OQPBYkEwn5-2-YL6bZPFt7Dn3W9qtr39rwOjC4rXI3VNL3XYO89b6qJu0UagQ__)

### Why azure databricks

We choose to use azure databricks instead of other azure AI services like semantic kernel, foundry etc because of the following reaons
- Azure Databricks' Scalable Spark Engine: Azure Databricks, leveraging its distributed Apache Spark engine within the Azure ecosystem, can efficiently process terabytes of logs in parallel – a scale unmatched by individual agent frameworks.
- Azure Databricks' Optimized Summarization Tools: Azure Databricks provides built-in, optimized functions and libraries within the Azure environment specifically for data aggregation, filtering, and transformation – crucial pre-processing steps for effective log summarization.
- Cost Efficiency of Azure Databricks for Large Data: For high-volume log summarization, Azure Databricks on Azure offers a more cost-effective solution compared to repeatedly feeding large log chunks to LLM APIs through other frameworks.
- Direct Large File Handling in Azure Databricks: Azure Databricks is architected to directly ingest and process entire large log files stored within Azure, avoiding the need for manual chunking often required by agent frameworks.
- Azure Databricks' Powerful Pre-processing on Azure: Running on Azure, Azure Databricks provides a robust environment for cleaning, structuring, and extracting key insights from raw Azure-stored logs before generating concise summaries.



## Impact

By automating the resolution of routine alerts, **Kasper significantly reduces the manual workload on on-call teams**.

For a mid-sized organization handles roughly **1,000 alerts per day**, almost **60% is automatable** — that's **600 incidents handled without human intervention** daily.

- ⏱️ Time Saved — `Equivalent to 3.5 Full-Time Engineers`

    - Each auto-resolved alert saves about **20 minutes** of engineering effort.

    - **Daily time savings:**: 600 alerts × 20 minutes = **12,000 minutes** = **200 hours/day**
    - **Monthly savings (30 days):**: 200 hours/day × 30 = **6,000 hours/month**


- 💰 People Cost Savings — `Up to $5.4M/Year`

  - **At $50/hour for an engineer:**
    - 6,000 hours × $50 = **$300,000/month** = **$3.6M/year**
  
  - **At $75/hour (fully loaded rate):**
    - 6,000 hours × $75 = **$450,000/month** = **$5.4M/year**

- ⚙️ Infra Savings — `Up to $216,000/year`

    Unresolved incidents often keep expensive resources (like compute-heavy workloads) running unnecessarily, burning idle CPU/GPU cycles.

    - **Average cost of idle infra per alert (CPU, GPU, storage, network):** ~$1–3 per alert/hour
    - **Assume 300 of the 600 auto-resolved alerts/day involve infra components left running**
    - **Estimate: $2/hour/alert × 1-hour delay**

        - **Daily compute savings:**:  300 alerts × $2 = **$600/day**
        - **Monthly compute savings:**: $600 × 30 = **$18,000/month** = **$216,000/year**

### 📈 Combined Annual Efficiency Gains

**Kasper can generate over `$5.6 million` in annual savings**, combining:
- Engineering time savings
- Reduced operational costs
- Lower infrastructure waste

## How Kasper fits the judging criteria

1. Innovation 
- Interesting Premise:->  Kasper tackles a significant and common pain point in IT operations – inefficient incident response. The idea of an AI-powered "incident commander" that goes beyond basic alerting offers a fresh perspective.
- Creative Implementation:->  Kasper's proposed use of Azure AI Agents and Large Language Models (LLMs) to understand incident narratives, diagnose root causes with precision, and even automate remediation demonstrates a creative application of AI technology. The integration with existing tools like PagerDuty and Slack to create a unified workflow further enhances this.
- Engaging Demo:->  A well-executed demo showcasing Kasper's ability to ingest alerts, provide insightful analysis, and automate or guide remediation will effectively highlight its innovative capabilities.

2. Impact 
- Would we use the project ourselves?:->  The potential for Kasper to significantly reduce manual workload, minimize downtime, and improve the efficiency of incident response makes it highly valuable for various organizations dealing with IT incidents. The quantifiable benefits (time savings, cost savings, infrastructure savings) strongly support its potential impact.
- Is the value/purpose of the project evident?:->  Kasper's purpose – to streamline and automate incident response using AI – is clearly articulated. The problem statement effectively highlights the challenges it aims to solve, and the solution directly addresses these issues with tangible benefits.

3. Usability 
- Does the project address a real-world scenario? How practical is the solution? :-> Kasper directly addresses the very real and common challenges faced by IT teams in managing incidents. By offering an automated and intelligent approach, it provides a practical solution to alert fatigue, context scarcity, and manual diagnostics.
- Does the project include sophisticated features such as Human-in-the-Loop?:->  Kasper incorporates a crucial human-in-the-loop mechanism for high-risk actions, ensuring that critical decisions are not fully automated and allowing for human oversight and intervention.
- Does the project incorporate Responsible AI practices? Kasper follows the 6 main pillars for responsible AI
    - Transparency: We aim for Kasper to explain its reasoning for diagnoses and recommendations clearly. Each steps has proper logging
    - Accountability:  Critical actions require human approval, preventing unchecked automation.
    - Reliability & Safety: Human oversight for critical actions, rigorous testing.
    - Security & Privacy: Incident data handling will adhere to security best practices and respect privacy.
    - Inclusiveness: Designed to aid all engineers with clear explanations.
    - Fairness (Future Consideration): We will actively consider and address potential biases in the data Kasper learns from as the system evolves.

4. Solution Quality 

- How complete is the project repository, README, and codebase?:->  We have a well-structured repository with clear documentation (README) explaining setup, usage, and architecture, along with a well-commented and robust codebase, will be crucial for demonstrating solution quality.
- Is there substantial technical implementation: We have a strong technical implementation. Details here

5. Alignment with hackathon category 

- Is the solution an agent built with either the corresponding programming language?:->  Kasper is built using a language like Python and js and leverages Azure AI Agents 
- How well does the project showcase the programming language or Microsoft technology of its category? We use different microsoft technologies liek azure databricks, azure openai, azure cosmos db, azure vector search etc

### Screenshots
![img1](https://media-hosting.imagekit.io/ce87e20e64204fbf/aa.png?Expires=1840605705&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=XlyzCDxKl1NEEnRvIDnw-Y6-2FebhYAvKoOpzPmqob2L2oK8zLKmnV2mp5DdSi2phIB8xoHcJV1TrfVto7hzinQwYI1TcPPA8zeW~NixhErOK1CP9hA~nj6UVhirZmpf7gmgCJE~MEndNvmPVfwBdI~aoOQN7V3A-0F~QZ4kgldVbrbUal7e0szGyx3GGyqtISXdYvZO5~nNp~ag~acq2ye4sarVW56n9FiumSaB5Ck6t6~KOeMRfKBY5I843UuoMcWIJfp9Q3Fbp-iwgglMnMKE5nPbEDw2QKiSfFdYe2PgTEiSAUL7fXX1b8wI1-5v8OskXyi1w8Qxe26yy-Xs9Q__)

![img](https://media-hosting.imagekit.io/5d93c8f2c24c4d95/1.png?Expires=1840605642&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=XDwG6B7re4dt2ai7DCm1pgdurxO-8AIW~tcpXdkd~VPj43NcNqjlKnln-d41GHEXkocfR1fJmRvL7cQFnsW0ouzBlr3ld-n5rw8Yd70cadplB1BY~mVGT1Lc140fFPy86Oi8rI8NvmTYEflnuIr0lu5ti0aHOvH41yhGD7kOCOO90nIZZxj5yuiSzX27WCqvJ1OeQjeY-AY0RcgwIwV21qLgkvzzIFwguyVNXT819gAMfcBo5K-D2eGbY5LmZBxXtRp94aC4jTzWsTXozoCBI8rZvEXc7OAMrznnlmPHoQ9R~aMBalXM95v3E04Ih4qxzZTbMN85BOIiFu8axiJgVA__)

![img](https://media-hosting.imagekit.io/8e00ba0549b84c2d/1.5.png?Expires=1840605644&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=UXg4mUzChZrM3TfaX3v1RogGcMbB-CjIsv5iZl6qjWiK4pp22kSW8IsbAf-4IdvM5BPfx3W8fFZ4yZvOr8u71LpIzYtPMSAkp4KAd5mnjnVi7GN8R-L5PfMLJSdUXS1JtsqnTs9ZowMawEOrKkQbz-BkiuYHrtylg8QQqRqf6s6Q9dhn9aSxfzEWqoMPPYlK51XoqZLwuVCa2QX8xos8EZd2tipWMoB1rW5g~o47OI19OzJfRXYhKvfTAliH2rojAYrxgGYjUXYB7D2ZjODcbboSTfkn3kyHocfQWjDsIuCIpniTuOwrOqfXeDQgbjX3JkQQe-XQ81rOSUlu0Xntyw__)

![img](https://media-hosting.imagekit.io/bb673c7c7b25482c/4.png?Expires=1840605647&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=ueS-Jt2zmhhKeWiSFX7wiGaLq828ddGDwStk4PMZ8S5F03nSe4Lvrsws1UtJHzc4V2bMXjkh91Lri~gkuz4nVXr~IOySE3s4CFbehSB4Os8YyzslwC9VmUaW137EiELnBetJEWxsZDOJKKXtniORJT8gsEavgf~ScPQYOs6xs1zER0rwwpzI0E2N~rO5ipBLZ9ajOJtbaHzP6jaHDH2N4MfoDkNiiA0Eo-3Hmx-jskfaX17S0LpFRMfOorEJSrXPhcb48LDMBx~RVQOAeit3iEaElzgofJG6U~w1X66r-4uoZB~-O2OAnftt7NKdifQDZnhXgCI0xFGiUBhE9AWh7g__)

![img](https://media-hosting.imagekit.io/fd868148719d482f/2.png?Expires=1840605857&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=odU1IVDAmdpuWeAAeo2CwuAbOs~TQU4TxT-1Hjf036pHAahWQtfcobnQ7Y5EcwoUW3e4RT9aknHxkCYPx8-U7Uc9Qx6cRlUf8EGjpcZ5TwTIezc6naLyRU6xqFzPG-3R2B-b1ImjVkjTv59vv55pX8y3q428fVmy8-4VAMpvDy~JIfQ3zNLSFPp8uHoy8NsyEqZzS1draSV4dNHqtcy4fcG4WyEpH01WR2AWHQxjgmAy5A92lvbqrL1qJLRieV2H6F35mlNFqj-7-lHwajGm~Sh5hXVY2dNepzjJ-F-RWJNltSaiMZSRESyxPDWaeFE4X8Ni6HMbU-t8vrCedz114Q__)

## Code Structure

### Frontend Structure
```
frontend/
├── src/
│   ├── components/          # Reusable React components
│   │   ├── LogsPanel/      # Log summary display component
│   │   ├── IncidentCard/   # Incident display component
│   │   └── RiskIndicator/  # Risk level visualization
│   ├── pages/              # Main application pages
│   │   ├── Dashboard/      # Main dashboard view
│   │   ├── Incidents/      # Incidents management view
│   │   └── Settings/       # Configuration settings
│   ├── services/           # API and external service integrations
│   │   ├── api.ts         # API client configuration
│   │   ├── slack.ts       # Slack integration
│   │   └── pagerduty.ts   # PagerDuty integration
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Utility functions
│   ├── App.tsx           # Main application component
│   └── main.tsx          # Application entry point
├── public/               # Static assets
├── package.json         # Dependencies and scripts
└── vite.config.ts       # Vite configuration
```

### Backend Structure
```
backend/
├── src/
│   ├── agents/           # Azure AI Agents implementation
│   │   ├── incident_commander.py  # Main incident handling agent
│   │   ├── log_analyzer.py       # Log analysis agent
│   │   └── risk_assessor.py      # Risk assessment agent
│   ├── integrations/     # External service integrations
│   │   ├── slack/       # Slack bot implementation
│   │   ├── pagerduty/   # PagerDuty API integration
│   │   └── azure/       # Azure services integration
│   ├── models/          # Data models and schemas
│   ├── services/        # Core business logic
│   │   ├── log_service.py       # Log aggregation service
│   │   ├── runbook_service.py   # Runbook management
│   │   └── risk_service.py      # Risk assessment service
│   ├── utils/           # Utility functions
│   └── main.py          # Application entry point
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
└── .env.example        # Environment variables template
```

### Key Components

#### Frontend Components
- **LogsPanel**: Displays aggregated logs with filtering and search capabilities
- **IncidentCard**: Shows incident details and status
- **RiskIndicator**: Visual representation of risk levels
- **Dashboard**: Main view with incident overview and metrics
- **Settings**: Configuration interface for integrations

#### Backend Services
- **Incident Commander**: Main agent orchestrating incident response
- **Log Analyzer**: Processes and summarizes log data
- **Risk Assessor**: Evaluates potential impact of actions
- **Log Service**: Handles log aggregation and analysis
- **Runbook Service**: Manages runbook storage and retrieval
- **Risk Service**: Implements risk assessment logic

#### Integration Points
- **Slack**: Real-time communication and notifications
- **PagerDuty**: Incident detection and management
- **Azure Services**: AI capabilities and data storage
  - Azure OpenAI: Natural language processing
  - Azure Databricks: Log analysis and processing
  - Azure Cosmos DB: Data persistence
  - Azure Vector Search: Runbook retrieval

## 🔧 Setup & Configuration

### Prerequisites
- Node.js 18+
- Python 3.11+
- Azure account with required services
- PagerDuty account
- Slack workspace

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Environment Variables

### Required Variables
```bash
# Slack Configuration
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_APP_TOKEN=your_slack_app_token

# PagerDuty Configuration
PAGERDUTY_API_KEY=your_pagerduty_api_key
PAGERDUTY_URL=your_pagerduty_url

# Azure Configuration
AZURE_DATABRICKS_ENDPOINT=your_databricks_endpoint
AZURE_DATABRICKS_TOKEN=your_databricks_token
AZURE_DATABRICKS_WAREHOUSE_ID=your_warehouse_id
AZURE_COSMO_DB=your_cosmos_db_connection_string
MONGO_DB_NAME=your_database_name

# Application Settings
COMMAND_TIMEOUT=300
```



### Registration Check

- [x] Each of my team members has filled out the registration form

