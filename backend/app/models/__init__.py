# Import all models here so SQLModel.metadata is populated for alembic autogenerate.
from app.models.dataset import Dataset, SalesRecord  # noqa: F401
from app.models.user import User  # noqa: F401

__all__ = ["User", "Dataset", "SalesRecord"]
