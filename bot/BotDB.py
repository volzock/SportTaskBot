from sqlalchemy import create_engine, insert, text, select, MetaData, Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker

class BotData:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        self.conn = self.engine.connect()
        self.metadata_obj = MetaData()
        self.create_bot_database()
        self.insert_default_roles()

    def create_bot_database(self):
        #conn.execute(f"CREATE TABLE public.user(id integer, telegram_id integer, name text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.user OWNER to {user};")
        user_table = Table(
            "user",
            self.metadata_obj,
            Column('id', Integer, primary_key = True),
            Column('telegram_id', Integer),
            Column('name', String),
            Column('surname', String),
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
        self.metadata_obj.create_all(self.engine)
        self.conn.commit()
        #conn.execute("SELECT * FROM public.role WHERE id=1")
    

    def insert_default_roles(self):
        role_table = Table("role", self.metadata_obj, autoload_with=self.engine)
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
    
    def insert_into_table(self, table_name: str, records: list):
        table = Table(table_name, self.metadata_obj, autoload_with=self.engine)
        self.conn.execute(insert(table), records)
        self.conn.commit()
    
    def sql_select_request(self, request: str) -> list:
        return self.conn.execute(text(request)).fetchall()
        
    def table_update(self, request: str):
        self.conn.execute(text(request))
        self.conn.commit()
    
    '''
    def select_from_table(self, table_name: str, where_parametrs: str):
        sql = "SELECT * FROM "+table_name+' WHERE '+where_parametrs 
        return self.conn.execute(text(sql)).fetchall()

    def update_in_table(self, table_name: str, records: list, where_parametrs: str):
        sql = "UPDATE "+table_name+' SET '+where_parametrs 
        self.conn.execute(text(sql))
        #self.conn.execute(update(table).where(exec("table.c.%s" % where_parametrs)), records)
    '''

'''
if __name__ == '__main__':
    bot_db = BotData("sqlite+pysqlite:///:memory:")
    bot_db.insert_into_table('user', [{'id': 546, 'telegram_id': 123, 'name': 'Test', 'surname': 'Test'}])
    print(bot_db.table_sql_request('SELECT * FROM user WHERE id = 546'))
 
''' 