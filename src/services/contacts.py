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
        """
        Create a new contact.

        Args:
            body (ContactCreate): The contact data for creation.
            user_id (int): The ID of the user creating the contact.

        Returns:
            ContactResponse: The created contact.
        """
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
        """
        Retrieve a list of contacts with optional filters.

        Args:
            skip (int): The number of contacts to skip.
            limit (int): The maximum number of contacts to return.
            user_id (int): The ID of the user to retrieve contacts for.
            name (Optional[str]): Optional filter by name.
            surname (Optional[str]): Optional filter by surname.
            email (Optional[str]): Optional filter by email.

        Returns:
            List[ContactResponse]: A list of contacts.
        """
        return await self.contact_repository.get_contacts(
            skip, limit, user, name, surname, email
        )

    async def get_contact(self, contact_id: int, user: User):
        """
        Retrieve a contact by its ID.

        Args:
            contact_id (int): The ID of the contact to retrieve.
            user_id (int): The ID of the user to retrieve the contact for.

        Returns:
            ContactResponse | None: The retrieved contact or None if not found.
        """
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactUpdate, user: User):
        """
        Update an existing contact.

        Args:
            contact_id (int): The ID of the contact to update.
            body (ContactUpdate): The updated contact data.
            user_id (int): The ID of the user updating the contact.

        Returns:
            ContactResponse | None: The updated contact or None if not found.
        """
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """
        Remove a contact.

        Args:
            contact_id (int): The ID of the contact to remove.
            user_id (int): The ID of the user removing the contact.

        Returns:
            ContactResponse | None: The removed contact or None if not found.
        """
        return await self.contact_repository.remove_contact(contact_id, user)

    async def get_upcoming_birthdays(self, user: User, days: int = 7):
        """
        Retrieve contacts with upcoming birthdays within a specified number of days.

        Args:
            user_id (int): The ID of the user to retrieve contacts for.
            days (int): The number of days to look ahead for upcoming birthdays. Default is 7.

        Returns:
            List[ContactResponse]: A list of contacts with upcoming birthdays.
        """
        return await self.contact_repository.get_upcoming_birthdays(user, days)
