from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class HealthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_db(self) -> bool:
        try:
            async with self.session.begin():
                await self.session.execute("SELECT 1")
            return True
        except SQLAlchemyError:
            return False
