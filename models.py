from pydantic import BaseModel
from datetime import datetime
from typing import Literal


WorkOrderStatus = Literal[
    "pending",
    "in_progress",
    "completed",
    "cancelled"
]


class WorkOrderCreate(BaseModel):
    title: str
    description: str | None = None


class WorkOrderStatusUpdate(BaseModel):
    status: WorkOrderStatus

class WorkOrderStatusResponse(BaseModel):
    work_order_id: int
    status: WorkOrderStatus

class WorkOrderResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: WorkOrderStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }