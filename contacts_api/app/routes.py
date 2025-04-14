from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud
from app.database import get_db
from app.schemas import ContactCreate, ContactUpdate, ContactOut

router = APIRouter()


@router.post("/", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_contact(contact, db)


@router.get("/", response_model=List[ContactOut])
async def get_contacts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_contacts(skip, limit, db)


@router.get("/{contact_id}", response_model=ContactOut)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await crud.get_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactOut)
async def update_contact(contact_id: int, updated: ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact = await crud.update_contact(contact_id, updated, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await crud.delete_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")


@router.get("/search/", response_model=List[ContactOut])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    return await crud.search_contacts(query, db)


@router.get("/birthdays/upcoming", response_model=List[ContactOut])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await crud.get_upcoming_birthdays(db)
