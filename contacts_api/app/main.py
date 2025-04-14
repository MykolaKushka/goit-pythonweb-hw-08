from fastapi import FastAPI
from app.routes import router as contacts_router

app = FastAPI(title="Contacts REST API")

app.include_router(contacts_router, prefix="/api/contacts", tags=["Contacts"])
