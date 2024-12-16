import json
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    User,
)
from src.services.contacts import ContactService
from src.services.auth import get_current_user
from src.redis import get_redis
from fastapi.encoders import jsonable_encoder

CACHE_TTL_SEC = 3600

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = Query(None),
    surname: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get all contacts for the current user with optional filters.

    Args:
        skip (int): The number of contacts to skip. Default is 0.
        limit (int): The maximum number of contacts to return. Default is 10.
        name (str): Optional filter by name.
        surname (str): Optional filter by surname.
        email (str): Optional filter by email.
        db (AsyncSession): The database session.
        user (User): The current authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(
        skip, limit, user, name, surname, email
    )

    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    redis=Depends(get_redis),
):
    """
    Get a contact by ID.

    Args:
        contact_id (int): The ID of the contact to retrieve.
        db (AsyncSession): The database session.
        user (User): The current authenticated user.

    Returns:
        ContactResponse: The retrieved contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    cache_key = f"contact:{contact_id}"
    cached_contact = await redis.get(cache_key)
    if cached_contact:
        print(f"Cache hit for {cache_key}")
        return ContactResponse.model_validate_json(cached_contact)

    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    await redis.set(cache_key, json.dumps(jsonable_encoder(contact)), ex=CACHE_TTL_SEC)
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    redis=Depends(get_redis),
):
    """
    Create a new contact.

    Args:
        contact_data (ContactCreate): The contact data for creation.
        db (AsyncSession): The database session.
        user (User): The current authenticated user.

    Returns:
        ContactResponse: The created contact.
    """
    contact_service = ContactService(db)
    contact = await contact_service.create_contact(body, user)
    cache_key = f"contact:{contact.id}"
    await redis.set(cache_key, json.dumps(jsonable_encoder(contact)), ex=CACHE_TTL_SEC)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactUpdate,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    redis=Depends(get_redis),
):
    """
    Update a contact.

    Args:
        contact_id (int): The ID of the contact to update.
        body (ContactUpdate): The updated contact data.
        db (AsyncSession): The database session.
        user (User): The current authenticated user.

    Returns:
        ContactResponse: The updated contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    cache_key = f"contact:{contact_id}"
    await redis.set(cache_key, json.dumps(jsonable_encoder(contact)), ex=CACHE_TTL_SEC)
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    redis=Depends(get_redis),
):
    """
    Remove a contact.

    Args:
        contact_id (int): The ID of the contact to remove.
        db (AsyncSession): The database session.
        user (User): The current authenticated user.

    Returns:
        ContactResponse: The removed contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    cache_key = f"contact:{contact_id}"
    await redis.delete(cache_key)
    return contact


@router.get("/birthdays/upcoming", response_model=List[ContactResponse])
async def get_upcoming_birthdays(
    days: int = Query(7),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get contacts with upcoming birthdays within a specified number of days.

    Args:
        days (int): The number of days to look ahead for upcoming birthdays. Default is 7.
        db (AsyncSession): The database session.
        user (User): The current authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts with upcoming birthdays.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_upcoming_birthdays(user, days)
    return contacts
