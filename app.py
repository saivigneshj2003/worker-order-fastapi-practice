from fastapi import FastAPI
from src.api.v1.work_orders import work_order_router

app = FastAPI()
app.include_router(work_order_router)