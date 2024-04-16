from fastapi import FastAPI

from app.bills import api as bills_api

app = FastAPI()

app.include_router(bills_api.router)
