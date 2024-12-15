from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate, User


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(
        self,
        body: ContactCreate,
        user: User,
    ):
        existing_contact = await self.contact_repository.get_contact_by_email(
            body.email, user
        )
        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Contact with this email already exists",
            )

        return await self.contact_repository.create_contact(body, user)

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        user: User,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None,
    ):
        return await self.contact_repository.get_contacts(
            skip, limit, user, name, surname, email
        )

    async def get_contact(self, contact_id: int, user: User):
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactUpdate, user: User):
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        return await self.contact_repository.remove_contact(contact_id, user)

    async def get_upcoming_birthdays(self, user: User, days: int = 7):
        return await self.contact_repository.get_upcoming_birthdays(user, days)
