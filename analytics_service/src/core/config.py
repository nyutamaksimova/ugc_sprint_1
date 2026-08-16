from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    kafka_bootstrap_servers: str = "kafka:9092"
    max_content_length: int = 1024 * 1024

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(jwt_secret_key=os.getenv("JWT_SECRET_KEY", "change-me"))
