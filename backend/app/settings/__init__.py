from app.settings.auth import AuthSettings
from app.settings.database import DatabaseSettings

db = DatabaseSettings()
auth = AuthSettings()

__all__ = ["db", "auth", "DatabaseSettings", "AuthSettings"]
