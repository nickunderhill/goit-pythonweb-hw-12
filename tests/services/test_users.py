import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.users import UserService
from src.repository.users import UserRepository
from src.schemas import User, UserCreate


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_user_repository(mock_db_session):
    return AsyncMock(spec=UserRepository, db=mock_db_session)


@pytest.fixture
def user_service(mock_db_session):
    return UserService(db=mock_db_session)


@pytest.mark.asyncio
async def test_create_user(user_service, mock_user_repository):
    user_data = UserCreate(
        username="test", email="test@example.com", password="password"
    )
    mock_user_repository.create_user.return_value = User(
        id=1, username="test", avatar="avatar_url", email="test@example.com"
    )

    with patch("src.services.users.Gravatar", autospec=True) as mock_gravatar:
        mock_gravatar.return_value.get_image.return_value = "avatar_url"
        user = await user_service.create_user(user_data)

    assert user.email == "test@example.com"
    assert user.username == "test"
    assert user.avatar == "avatar_url"


@pytest.mark.asyncio
async def test_create_user_with_exception(user_service, mock_user_repository):
    user_data = UserCreate(
        username="test", email="test@example.com", password="password"
    )
    mock_user_repository.create_user.return_value = User(
        id=1, username="test", avatar="avatar_url", email="test@example.com"
    )

    with patch("src.services.users.Gravatar", side_effect=Exception):
        result = await user_service.create_user(user_data)

    assert result.email == "test@example.com"
    assert result.username == "test"
    assert result.avatar is None


async def test_get_user_by_email(user_service, mock_user_repository):
    # Create a user instance to return
    user = User(id=1, username="test", avatar="avatar", email="test@example.com")

    # Mock the repository's async method
    mock_user_repository.get_user_by_email = AsyncMock(return_value=user)

    # Call the service method
    result = await user_service.get_user_by_email("test@example.com")

    # Assertions
    assert result.username == "test"
