from dishka import Provider

from .config import ConfigProvider
from .db import DbProvider
from .fast_stream import FastStreamAppProvider


def get_providers() -> list[Provider]:
    return [
        ConfigProvider(),
        DbProvider(),
        FastStreamAppProvider()
    ]