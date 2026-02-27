# Import all models here so SQLModel.metadata is populated for alembic autogenerate.
from app.models.user import User  # noqa: F401

__all__ = ["User"]
