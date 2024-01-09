from sqlalchemy import create_engine, insert, text, ForeignKey, Column, Integer, String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    """
    Используй TELEGRAM_ID в качестве Primary_key 
    """
    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    def __repr__(self) -> str:
        return f"User(telegram_id = {self.telegram_id!r}, name={self.name!r}, surname={self.surname!r})"


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"


class Service(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]

    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, url={self.url!r})"


class ServiceData(Base):
    __tablename__ = "service_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password: Mapped[str]
    url: Mapped[str]
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))

    def __repr__(self) -> str:
        return f"ServiceData"


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    status: Mapped[bool]

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, url={self.url!r}, topic_id={self.topic_id!r}, service_id={self.service_id!r}, status={self.status!r})"


class Sumbition(Base):
    __tablename__ = "sumbition"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.telegram_id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    status: Mapped[str]

    def __repr__(self) -> str:
        return f"Sumbiotion(id={self.id!r}, user_id={self.user_id!r}, task_id={self.task_id!r}, status={self.status!r})"


