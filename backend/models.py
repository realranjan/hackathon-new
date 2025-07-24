from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "viewer"
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class UserRegisterResponse(BaseModel):
    message: str
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    id: int
    email: EmailStr
    role: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

class ShipmentUpdateRequest(BaseModel):
    product_id: str
    current_location: Optional[str] = None
    status: Optional[str] = None
    legs: Optional[List[Any]] = None

class ShipmentUpdateResponse(BaseModel):
    updated_shipment: Dict[str, Any]

class DisruptionEvent(BaseModel):
    location: str
    event_type: str
    severity: str
    timestamp: str
    source: str
    mode: Optional[str] = None

class AlertResponse(BaseModel):
    alerts: List[Dict[str, Any]]

class RiskReportRequest(BaseModel):
    disruptions: List[Dict[str, Any]]

class RiskReportResponse(BaseModel):
    risk_report: List[Dict[str, Any]]

class GenAIPlanRequest(BaseModel):
    risk_report: List[Dict[str, Any]]

class GenAIPlanResponse(BaseModel):
    action_plan: List[Dict[str, Any]]