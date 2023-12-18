from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class CurrentRate(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    currency_name: Mapped[str] = mapped_column(String(40), nullable=False)
    value: Mapped[float]
