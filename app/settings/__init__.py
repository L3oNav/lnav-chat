from .settings import *
from app.settings.settings import Settings
from .redis import r
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
