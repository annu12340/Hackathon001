from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Incident(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    assigned_to: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class AlertHistory(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    incident_id: str
    alert_type: str
    alert_message: str
    alert_source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False
    metadata: dict = Field(default_factory=dict)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class RemediationStep(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    incident_id: str
    step_number: int
    description: str
    status: str
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        } 