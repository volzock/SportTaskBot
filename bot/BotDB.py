from sqlalchemy import create_engine, insert, text, select, MetaData, Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column
    
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    telegram_id: Mapped[int]
    name: Mapped[str]
    surname: Mapped[str]
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, telegram_id = {self.telegram_id!r}, name={self.name!r}, surname={self.surname!r})"

class Role(Base):
    __tablename__ = "role"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"

class RoleUser(Base):
    __tablename__ = "role_table"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    
    def __repr__(self) -> str:
        return f"RoleUser(user_id={self.user_id!r}, role_id={self.role_id!r})"

class Topic(Base):
    __tablename__ = "topic"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Topic(id={self.id!r}, name={self.name!r})"
    
class Service(Base):
    __tablename__ = "service"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    url: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, url={self.url!r})"

class Task(Base):
    __tablename__ = "task"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    url: Mapped[str]
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    status: Mapped[bool]
    
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, url={self.url!r}, topic_id={self.topic_id!r}, service_id={self.service_id!r}, status={self.status!r})"
    

class Sumbition(Base):
    __tablename__ = "sumbition"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    status: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Sumbiotion(id={self.id!r}, user_id={self.user_id!r}, task_id={self.task_id!r}, status={self.status!r})"

class BotData:
    def __init__(self, url):
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)
    
    def insert_into_table(self, table_name, records: list):
        self.session.execute(insert(table_name), records)
        
    def table_sql_request(self, request):
        return self.session.execute(text(request)).all()
     

'''
if __name__ == '__main__':
    bot_db = BotData("sqlite+pysqlite:///:memory:")
    bot_db.insert_into_table(User, [{'id': 546, 'telegram_id': 123, 'name': 'Test', 'surname': 'Test'}])
    print(bot_db.table_sql_request("SELECT * FROM user WHERE id = 546"))
 
'''