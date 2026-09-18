from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.work_orders import work_order_router
from src.database.connection import engine, Base
from src.database.models import WorkOrder


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Close database connections
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(work_order_router)