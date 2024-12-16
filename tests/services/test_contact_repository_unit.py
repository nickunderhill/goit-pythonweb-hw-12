import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository

from src.database.models import Contact, User
from src.schemas import ContactUpdate, ContactCreate
from datetime import datetime, date


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def contact_repository(mock_session):
    return ContactRepository(mock_session)


@pytest.fixture
def user():
    return User(id=1, username="testuser", email="test@email.com", avatar="avatar")


@pytest.mark.asyncio
async def test_get_contact_by_id(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1,
        name="John",
        surname="Doe",
        email="john@doe.com",
        phone="123",
        birthday=datetime(2012, 1, 15, 12, 0, 0),
        additional_info="info",
        user=user,
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.get_contact_by_id(contact_id=1, user=user)

    # Assertions
    assert result is not None
    assert result.id == 1
    assert result.name == "John"
    assert result.surname == "Doe"
    assert result.email == "john@doe.com"
    assert result.phone == "123"
    assert result.birthday == datetime(2012, 1, 15, 12, 00, 00)
    assert result.additional_info == "info"


@pytest.mark.asyncio
async def test_get_contact_by_email(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1,
        name="John",
        surname="Doe",
        email="john@doe.com",
        phone="123",
        birthday=datetime(2012, 1, 15, 12, 0, 0),
        additional_info="info",
        user=user,
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.get_contact_by_email(
        email="john@doe.com", user=user
    )

    # Assertions
    assert result is not None
    assert result.id == 1
    assert result.name == "John"
    assert result.surname == "Doe"
    assert result.email == "john@doe.com"
    assert result.phone == "123"
    assert result.birthday == datetime(2012, 1, 15, 12, 00, 00)
    assert result.additional_info == "info"


@pytest.mark.asyncio
async def test_get_contacts(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(
            id=1,
            name="John",
            surname="Doe",
            email="john@doe.com",
            phone="123",
            birthday=datetime(2012, 1, 15, 12, 0, 0),
            additional_info="info",
            user=user,
        )
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.get_contacts(skip=0, limit=10, user=user)

    # Assertions
    assert len(result) == 1
    assert result[0].name == "John"


@pytest.mark.asyncio
async def test_update_contact(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1,
        name="John",
        surname="Doe",
        email="john@doe.com",
        phone="123",
        birthday=datetime(2012, 1, 15, 12, 0, 0),
        additional_info="info",
        user=user,
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.update_contact(
        contact_id=1,
        body=ContactUpdate(
            name="Jane",
            surname="Doe",
            email="jane@doe.com",
            phone="123",
            birthday=date(2012, 1, 15),
            additional_info="info",
        ),
        user=user,
    )

    # Assertions
    assert result is not None
    assert result.id == 1
    assert result.name == "Jane"
    assert result.email == "jane@doe.com"


@pytest.mark.asyncio
async def test_remove_contact(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1,
        name="John",
        surname="Doe",
        email="john@doe.com",
        phone="123",
        birthday=datetime(2012, 1, 15, 12, 0, 0),
        additional_info="info",
        user=user,
    )

    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.remove_contact(contact_id=1, user=user)

    # Assertions
    assert result is not None
    assert result.id == 1
    assert result.name == "John"
    assert result.email == "john@doe.com"


@pytest.mark.asyncio
async def test_get_upcoming_birthdays(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(
            id=1,
            name="John",
            surname="Doe",
            email="john@doe.com",
            phone="123",
            birthday=datetime(2012, 1, 15, 12, 0, 0),
            additional_info="info",
            user=user,
        )
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.get_upcoming_birthdays(user=user)

    # Assertions
    assert len(result) == 1
    assert result[0].name == "John"
    assert result[0].surname == "Doe"


@pytest.mark.asyncio
async def test_create_contact(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1,
        name="John",
        surname="Doe",
        email="john@doe.com",
        phone="123",
        birthday=datetime(2012, 1, 15, 12, 0, 0),
        additional_info="info",
        user=user,
    )

    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.create_contact(
        body=ContactCreate(
            name="John",
            surname="Doe",
            email="john@doe.com",
            phone="123",
            birthday=date(2012, 1, 15),
            additional_info="info",
        ),
        user=user,
    )

    # Assertions
    assert result is not None
    assert result.id == 1
    assert result.name == "John"
    assert result.email == "john@doe.com"
    assert result.user == user
