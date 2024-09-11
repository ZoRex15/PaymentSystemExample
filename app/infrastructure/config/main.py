from typing import Any

import yaml

from app.infrastructure.config.models import Config
from app.infrastructure.config.service.parsers import (
    get_database_config,
    get_nats_config,
)

def load_config() -> Config:
    with open('config_dist/.settings.yml') as file:
        data: dict[str, Any] = yaml.safe_load(file)
        return Config(
            db=get_database_config(data.get('db')),
            nats=get_nats_config(data.get('nats'))
        )