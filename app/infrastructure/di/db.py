from typing import AsyncIterable

from dishka import Provider, provide, Scope

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine, create_async_engine

from app.infrastructure.config import Config
from app.infrastructure.db import HolderRepository


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, config: Config) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(config.db.url)
        yield engine
        engine.dispose(True)
        
    @provide
    async def get_poll(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)
    
    @provide(scope=Scope.REQUEST)
    async def get_session(self, poll: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with poll() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_repository(self, session: AsyncSession) -> HolderRepository:
        return HolderRepository(session)