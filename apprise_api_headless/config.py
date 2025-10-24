from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    apprise_config_dir: str = ".tmp/apprise_config"
