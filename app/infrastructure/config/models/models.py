from dataclasses import dataclass


@dataclass
class NATS:
    port: int
    host: str

    def __post_init__(self):
        self.url = f'nats://{self.host}:{self.port}'

@dataclass
class Database:
    user: str
    name: str
    host: str
    port: int
    password: str
    scheme: str

    def __post_init__(self):
        self.url = f'{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

@dataclass
class Config:
    nats: NATS
    db: Database