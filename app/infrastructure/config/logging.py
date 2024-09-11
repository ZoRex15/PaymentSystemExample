import logging.config

import yaml


logger = logging.getLogger(__name__)

def setup_logging() -> None:
    with open('config_dist/logging.yml', 'rt') as file:
        log_config = yaml.safe_load(file)
        logging.config.dictConfig(log_config)