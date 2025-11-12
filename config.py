from dataclasses import dataclass

from environs import env


@dataclass
class Db:
    host: str
    port: str
    name: str
    user: str
    password: str


@dataclass
class Config:
    db: Db


def load_config(path: str | None = None) -> Config:
    """Load the config"""
    env.read_env(path)
    return Config(
        db=Db(
            host=env.str("DB_HOST", "localhost"),
            port=env.str("DB_PORT", "5432"),
            name=env.str("DB_NAME", "postgres"),
            user=env.str("DB_USER", "postgres"),
            password=env.str("DB_PASS", "postgres"),
        )
    )
