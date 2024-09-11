import logging

from faststream import BaseMiddleware


logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def on_receive(self):
        logger.debug('Starting to process message: %s', self.msg)
        return await super().on_receive()
    
    async def after_processed(self, exc_type, exc_val, exc_tb):
        logger.debug('Finished processing message: %s', self.msg)
        return await super().after_processed(exc_type, exc_val, exc_tb)
