from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from src.database.connection import get_db
from src.database.models import WorkOrder
from models import (
    WorkOrderCreate,
    WorkOrderResponse,
    WorkOrderStatusUpdate,
    WorkOrderStatusResponse,
)

work_order_router = APIRouter(prefix="/api/v1")


# GET ALL WORK ORDERS
@work_order_router.get(
    "/work-orders",
    response_model=List[WorkOrderResponse]
)
async def get_work_orders(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkOrder)
    )

    work_orders = result.scalars().all()

    return work_orders



# GET WORK ORDER BY ID
@work_order_router.get(
    "/work-orders/{work_order_id}",
    response_model=WorkOrderResponse
)
async def get_work_order_id(
    work_order_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkOrder)
        .where(WorkOrder.id == work_order_id)
    )

    work_order = result.scalar_one_or_none()

    if not work_order:
        raise HTTPException(
            status_code=404,
            detail=f"Work order with id {work_order_id} not found"
        )

    return work_order


# GET WORK ORDER STATUS
@work_order_router.get(
    "/work-orders/{work_order_id}/status",
    response_model=WorkOrderStatusResponse
)
async def get_work_order_status(
    work_order_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkOrder)
        .where(WorkOrder.id == work_order_id)
    )

    work_order = result.scalar_one_or_none()

    if not work_order:
        raise HTTPException(
            status_code=404,
            detail=f"Work order with id {work_order_id} not found"
        )

    return {
        "work_order_id": work_order.id,
        "status": work_order.status
    }


# UPDATE WORK ORDER STATUS
@work_order_router.patch(
    "/work-orders/{work_order_id}/status",
    response_model=WorkOrderResponse
)
async def update_work_order_status(
    work_order_id: int,
    status_update: WorkOrderStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(WorkOrder)
            .where(WorkOrder.id == work_order_id)
        )

        work_order = result.scalar_one_or_none()

        if not work_order:
            raise HTTPException(
                status_code=404,
                detail=f"Work order with id {work_order_id} not found"
            )

        work_order.status = status_update.status

        await db.commit()
        await db.refresh(work_order)

        return work_order

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update work order status: {str(e)}"
        )


# CREATE WORK ORDER
@work_order_router.post(
    "/work-orders",
    response_model=WorkOrderResponse
)
async def add_work_order(
    work_order: WorkOrderCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        new_work_order = WorkOrder(
            **work_order.model_dump()
        )

        db.add(new_work_order)

        await db.commit()
        await db.refresh(new_work_order)

        return new_work_order

    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create work order: {str(e)}"
        )