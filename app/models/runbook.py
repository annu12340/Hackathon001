from pydantic import BaseModel, Field
from typing import List, Optional

class Runbook(BaseModel):
    """Model representing a runbook for incident resolution."""
    id: str = Field(..., description="Unique identifier for the runbook")
    title: str = Field(..., description="Title of the runbook")
    content: str = Field(..., description="Detailed resolution steps")
    category: str = Field(..., description="Category of the incident")
    severity: str = Field(..., description="Severity level (low, medium, high, critical)")
    tags: List[str] = Field(default_factory=list, description="Tags for better searchability")
    last_updated: str = Field(..., description="Last update timestamp")
    created_by: str = Field(..., description="Author of the runbook")
    content_vector: Optional[List[float]] = Field(None, description="Vector representation of the content")

    class Config:
        schema_extra = {
            "example": {
                "id": "rb-001",
                "title": "Database Connection Timeout",
                "content": "1. Check database connection pool\n2. Verify network connectivity\n3. Restart database service",
                "category": "Database",
                "severity": "high",
                "tags": ["database", "connection", "timeout"],
                "last_updated": "2024-01-01T12:00:00Z",
                "created_by": "admin"
            }
        } 