from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class ContactBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    birthday: Optional[date] = None
    additional_info: Optional[str] = Field(None, max_length=250)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True
