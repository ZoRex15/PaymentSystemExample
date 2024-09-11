import asyncio
from logging import getLogger

from dishka import make_async_container
from faststream import FastStream

from app.infrastructure.di import get_providers
from app.infrastructure.config.logging import setup_logging

logger = getLogger(__name__)

async def main():
    try:
        setup_logging()
        dishka = make_async_container(*get_providers())
        app = await dishka.get(FastStream)
        await app.run()
    except Exception as error:
        logger.critical('app close', error)
        await dishka.close()

if __name__ == '__main__':
    asyncio.run(main())