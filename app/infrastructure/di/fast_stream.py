from typing import AsyncIterable

import logging

from dishka import Provider, provide, Scope, AsyncContainer
from dishka.integrations.faststream import setup_dishka

from faststream.nats import NatsBroker
from faststream import FastStream

from app.infrastructure.config import Config
from app.infrastructure.broker.consumers import master_router
from app.infrastructure.broker.middlewares import CheckMiddleware, LoggingMiddleware

logger = logging.getLogger(__name__)


class FastStreamAppProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_app(self, dishka: AsyncContainer, broker: NatsBroker) -> AsyncIterable[FastStream]:
        app = FastStream(broker, logger=logger)
        setup_dishka(dishka, app, auto_inject=True)
        yield app
        await app.stop()

    @provide
    async def get_nats_broker(self, config: Config) -> NatsBroker:
        broker = NatsBroker(
            servers=(config.nats.url, ),
            middlewares=[CheckMiddleware, LoggingMiddleware],
            logger=logger
        )
        broker.include_router(master_router)
        return broker