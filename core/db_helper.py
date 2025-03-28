from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from core.config import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=True,
            expire_on_commit=False,
            autocommit=False,
        )

    def get_scoped_session(self):  # Создание сессии
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task  # TODO ?Пространство сессии?
        )
        return session

    async def session_dependency(self) -> AsyncSession:  # Передача сессии в нужные функции
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DataBaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
