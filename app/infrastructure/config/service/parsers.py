from typing import Any

from app.infrastructure.config.models import Database, NATS


def get_database_config(data: dict[str, Any]) -> Database:
    return Database(
        user=data.get('user'),
        name=data.get('name'),
        host=data.get('host'),
        port=int(data.get('port')),
        password=data.get('password'),
        scheme=data.get('scheme')
    )

def get_nats_config(data: dict[str, Any]) -> NATS:
    return NATS(
        port=int(data.get('port')),
        host=data.get('host')
    )
