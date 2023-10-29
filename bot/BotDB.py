from sqlalchemy import create_engine, insert, text, select, MetaData, Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker

class BotData:
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        self.conn = self.engine.connect()
        self.metadata_obj = MetaData()

    def create_bot_database(self):
        #conn.execute(f"CREATE TABLE public.user(id integer, telegram_id integer, name text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.user OWNER to {user};")
        user_table = Table(
            "user",
            self.metadata_obj,
            Column('id', Integer, primary_key = True),
            Column('telegram_id', Integer),
            Column('name', String),
        )
    
        #conn.execute(f"CREATE TABLE public.role(id integer, name text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.role OWNER to {user};")
        role_table = Table(
            "role",
            self.metadata_obj,
            Column('id', Integer, primary_key = True),
            Column('name', String),
        )
    
        #conn.execute(f"CREATE TABLE public.role_user(user_id integer, role_id integer); ALTER TABLE IF EXISTS public.role_user OWNER to {user};")
        role_user_table = Table(
            "role_user",
            self.metadata_obj,
            Column('user_id', Integer, ForeignKey("user.id"), nullable=False),
            Column('role_id', Integer, ForeignKey("role.id"), nullable=False),
        )
    
        #conn.execute(f"CREATE TABLE public.topic(id integer, name text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.topic OWNER to {user};")
        topic_table = Table(
            "topic",
            self.metadata_obj,
            Column('id', Integer, primary_key = True),
            Column('name', String),
        )
    
    #conn.execute(f"CREATE TABLE public.service(id integer, url text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.service OWNER to {user};")
    service_table = Table(
        "service",
        self.metadata_obj,
        Column('id', Integer, primary_key = True),
        Column('url', String),
    )
    
    #conn.execute(f"CREATE TABLE public.task(id integer, url text, topic_id integer, service_id integer, status boolean, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.task OWNER to {user};")
    task_table = Table(
        "task",
        self.metadata_obj,
        Column('id', Integer, primary_key = True),
        Column('url', String),
        Column('topic_id', Integer, ForeignKey("topic.id"), nullable=False),
        Column('service_id', Integer, ForeignKey("service.id"), nullable=False),
        Column('status', Boolean),
    )
    
    #conn.execute(f"CREATE TABLE public.sumbition(id integer, user_id integer, task_id integer, status text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.sumbition OWNER to {user};")
    sumbition_table = Table(
        "sumbition",
        self.metadata_obj,
        Column('id', Integer, primary_key = True),
        Column('user_id', Integer, ForeignKey("user.id"), nullable=False),
        Column('task_id', Integer, ForeignKey("task.id"), nullable=False),
        Column('status', String),
    )
    self.metadata_obj.create_all(engine)
    self.conn.commit()
    #conn.execute("SELECT * FROM public.role WHERE id=1")
    

def insert_default_roles(self):
    role_table = Table("role", self.metadata_obj, autoload_with=engine)
    s = select(role_table).where(role_table.c.id == 1)
    result = self.conn.execute(s)
    rec = list(result.fetchall())
    #print(rec)
    if rec == []:
        #conn.execute("INSERT INTO public.role(id, name) VALUES (1, admin);")
        s = insert(role_table).values(id = 1, name = 'admin')
        self.conn.execute(s)
        self.conn.commit()
    #conn.execute("SELECT * FROM public.role WHERE id=2")
    s = select(role_table).where(role_table.c.id == 2)
    rec = list(self.conn.execute(s).fetchall())
    if rec == []:
        #conn.execute("INSERT INTO public.role(id, name) VALUES (2, student);")
        s = insert(role_table).values(id = 2, name = 'student')
        self.conn.execute(s)
        self.conn.commit()
    #cursor.execute("SELECT * FROM public.role WHERE id=3")
    s = select(role_table).where(role_table.c.id == 3)
    rec = list(self.conn.execute(s).fetchall())
    if rec == []:
        #conn.execute("INSERT INTO public.role(id, name) VALUES (3, contestant);")
        s = insert(role_table).values(id = 3, name = 'contestant')
        self.conn.execute(s)
        self.conn.commit()

    
    
    
 