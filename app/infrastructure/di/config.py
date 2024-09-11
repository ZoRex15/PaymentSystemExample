from dishka import Provider, provide, Scope

from app.infrastructure.config import Config, load_config



class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self) -> Config:
        return load_config()