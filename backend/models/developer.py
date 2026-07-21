from datetime import time

from sqlalchemy import String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.models.base import TimestampMixin, UUIDMixin


class Developer(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "developers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="UTC")
    working_hours_start: Mapped[time | None] = mapped_column(Time, nullable=True)
    working_hours_end: Mapped[time | None] = mapped_column(Time, nullable=True)

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_assignments",
        back_populates="developers",
    )
