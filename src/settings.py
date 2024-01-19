from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_protocol: str = "postgresql+asyncpg"
    db_user: str = "postgres"
    db_name: str = "funny_dolphine"
    db_port: int = 5432
    db_host: str = "postgres"

    postgres_password: str

    isolation_level: str = "REPEATABLE READ"
    pool_size: int = 20
    max_overflow: int = 5
    auto_flush: bool = False
    expire_on_commit: bool = False

    model_config = ConfigDict(
        extra="allow",
    )


class AppSettings(BaseSettings):
    """
    Settings for the whole application.
    """

    app_env: str = "prod"

    debug: bool = False

    jwt_secret_key: str
    admin_password: str
    api_key: str

    database: DatabaseSettings = DatabaseSettings(
        _env_file="db.env", _env_file_encoding="utf-8"
    )

    def get_database_uri(self) -> str:
        return (
            f"{self.database.db_protocol}://"
            f"{self.database.db_user}:{self.database.postgres_password}@"
            f"{self.database.db_host}:{self.database.db_port}/{self.database.db_name}"
        )

    model_config = ConfigDict(
        extra="allow",
    )


settings = AppSettings(_env_file="web.env", _env_file_encoding="utf-8")
