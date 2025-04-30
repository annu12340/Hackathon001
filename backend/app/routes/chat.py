from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.databricks_service import DatabricksService

router = APIRouter()
databricks_service = DatabricksService()

class ChatQuery(BaseModel):
    message: str

@router.post("/query")
async def process_chat_query(query: ChatQuery):
    try:
        # Process the query through Databricks
        result = await databricks_service.process_query(query.message)
        
        return {
            "status": "success",
            "data": result,
            "message": "Query processed successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        ) 