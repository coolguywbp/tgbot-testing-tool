import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool

@dataclass
class PyrogramClient:
    name: str
    api_id: int
    api_hash: str
    phone_number: str
    session_string: str

@dataclass
class Config:
    tg_bot: TgBot
    pyrogram_client: PyrogramClient
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    pyrogram_client = config["pyrogram_client"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"]),
            use_redis=cast_bool(tg_bot.get("use_redis")),
        ),
        db=DbConfig(**config["db"]),
        pyrogram_client=PyrogramClient(
            name=pyrogram_client["name"],
            api_id=int(pyrogram_client["api_id"]),
            api_hash=pyrogram_client["api_hash"],
            phone_number=pyrogram_client["phone_number"],
            session_string=pyrogram_client["session_string"]
        )
    )
