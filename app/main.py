from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Automated Incident Resolution System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to verify the application is running."""
    return {"status": "ok", "message": "Automated Incident Resolution System is running"}

@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle incoming Slack events and PagerDuty alerts."""
    try:
        # TODO: Implement Slack event handling
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing Slack event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/slack/commands")
async def slack_commands(request: Request):
    """Handle Slack slash commands."""
    try:
        # TODO: Implement Slack command handling
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing Slack command: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 