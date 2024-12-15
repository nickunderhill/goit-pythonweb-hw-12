from sqlalchemy.ext.asyncio import AsyncSession

from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas import UserCreate


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """
        Create a new user.

        Args:
            user_data (UserCreate): The user data for creation.

        Returns:
            User: The created user.
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The retrieved user or None if not found.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User | None: The retrieved user or None if not found.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """
        Retrieve a user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User | None: The retrieved user or None if not found.
        """
        return await self.repository.get_user_by_email(email)

    async def update_avatar_url(self, email: str, url: str):
        """
        Update the avatar URL of a user.

        Args:
            email (str): The email of the user to update.
            avatar_url (str): The new avatar URL.

        Returns:
            User: The updated user with the new avatar URL.

        Raises:
            HTTPException: If the user is not found.
        """
        return await self.repository.update_avatar_url(email, url)
