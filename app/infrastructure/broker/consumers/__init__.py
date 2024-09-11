from faststream.nats import NatsRouter

from .payment_info import router as payment_info_router
from .payment import router as payments_royter

master_router = NatsRouter(prefix='payments.')
master_router.include_routers(
    payment_info_router,
    payments_royter
)

__all__ = [
    'master_router',
]