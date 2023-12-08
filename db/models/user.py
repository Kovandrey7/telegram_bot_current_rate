import uuid

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class User(Base):

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(String(40), nullable=False)
    subscribe: Mapped[bool] = mapped_column(Boolean, default=False)
