from faststream import BaseMiddleware


class CheckMiddleware(BaseMiddleware):
    async def on_receive(self):
        if self.msg.reply:
            return await super().on_receive()
        return None
    
    async def after_processed(self, exc_type, exc_val, exc_tb):
        return await super().after_processed(exc_type, exc_val, exc_tb)