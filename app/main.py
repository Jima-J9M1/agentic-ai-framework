from fastapi import FastAPI
from app.api import router
app = FastAPI(title="Production Agent Backend")

app.include_router(router)
