from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from app.models import Contact
from app.schemas import ContactCreate, ContactUpdate
from datetime import date, timedelta


# Створити контакт
async def create_contact(contact: ContactCreate, db: AsyncSession) -> Contact:
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact


# Отримати список всіх контактів
async def get_contacts(skip: int, limit: int, db: AsyncSession):
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()


# Отримати контакт за id
async def get_contact(contact_id: int, db: AsyncSession):
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    return result.scalar_one_or_none()


# Оновити контакт
async def update_contact(contact_id: int, updated: ContactUpdate, db: AsyncSession):
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if contact:
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(contact, key, value)
        await db.commit()
        await db.refresh(contact)
    return contact


# Видалити контакт
async def delete_contact(contact_id: int, db: AsyncSession):
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


# Пошук за іменем, прізвищем або email
async def search_contacts(query: str, db: AsyncSession):
    result = await db.execute(
        select(Contact).where(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
    )
    return result.scalars().all()


# Контакти з днями народження на найближчі 7 днів
async def get_upcoming_birthdays(db: AsyncSession):
    today = date.today()
    in_seven_days = today + timedelta(days=7)

    result = await db.execute(
        select(Contact).where(
            Contact.birthday.isnot(None),
            Contact.birthday.between(today, in_seven_days)
        )
    )
    return result.scalars().all()
