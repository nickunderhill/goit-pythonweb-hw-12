from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactUpdate, ContactCreate, User


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        user: User,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None,
    ) -> List[Contact]:
        stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
        if name:
            stmt = stmt.filter(Contact.name.ilike(f"%{name}%"))
        if surname:
            stmt = stmt.filter(Contact.surname.ilike(f"%{surname}%"))
        if email:
            stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_contact_by_id(
        self,
        contact_id: int,
        user: User,
    ) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id).filter_by(user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def get_contact_by_email(
        self,
        email: str,
        user: User,
    ) -> Contact | None:
        stmt = select(Contact).filter_by(email=email).filter_by(user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactCreate, user: User) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        contact = await self.get_contact_by_id(contact.id, user)
        if contact is None:
            raise ValueError("Contact not found")
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdate, user: User
    ) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id).filter_by(user=user)
        result = await self.db.execute(stmt)
        contact = result.scalar_one_or_none()
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthdays(self, user: User, days: int = 7) -> List[Contact]:
        today = datetime.today()
        upcoming_date = today + timedelta(days=days)

        stmt = (
            select(Contact)
            .filter(
                (extract("month", Contact.birthday) == today.month)
                & (extract("day", Contact.birthday) >= today.day)
                | (extract("month", Contact.birthday) == upcoming_date.month)
                & (extract("day", Contact.birthday) <= upcoming_date.day)
            )
            .filter_by(user=user)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
