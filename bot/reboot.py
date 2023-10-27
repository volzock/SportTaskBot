import psycopg2
 
#URL = "http://127.0.0.1:5000"

def create_database(user):
    cursor.execute("CREATE DATABASE bot_db WITH OWNER = postgres ENCODING = 'UTF8' CONNECTION LIMIT = -1;")
    cursor.execute(f"CREATE TABLE public.user(id integer, telegram_id integer, name text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.user OWNER to {user};")
    cursor.execute(f"CREATE TABLE public.role(id integer, name text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.role OWNER to {user};")
    cursor.execute(f"CREATE TABLE public.role_user(user_id integer, role_id integer); ALTER TABLE IF EXISTS public.role_user OWNER to {user};")
    cursor.execute(f"CREATE TABLE public.task(id integer, url text, topic_id integer, service_id integer, status boolean, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.task OWNER to {user};")
    cursor.execute(f"CREATE TABLE public.service(id integer, url text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.service OWNER to {user};")
    cursor.execute(f"CREATE TABLE public.sumbition(id integer, user_id integer, task_id integer, status text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.sumbition OWNER to {user};")
    cursor.execute(f"CREATE TABLE public.topic(id integer, name text, PRIMARY KEY (id)); ALTER TABLE IF EXISTS public.topic OWNER to {user};")

def insert_default_roles():
    cursor.execute("SELECT * FROM public.role WHERE id=1")
    rec = list(cursor.fetchall())
    if rec == []:
        cursor.execute("INSERT INTO public.role(id, name) VALUES (1, admin);")
    cursor.execute("SELECT * FROM public.role WHERE id=2")
    rec = list(cursor.fetchall())
    if rec == []:
        cursor.execute("INSERT INTO public.role(id, name) VALUES (2, student);")
    cursor.execute("SELECT * FROM public.role WHERE id=3")
    rec = list(cursor.fetchall())
    if rec == []:
        cursor.execute("INSERT INTO public.role(id, name) VALUES (3, contestant);")
    print("Done")

def insert_admin(username, telegram_id):
    cursor.execute(f"SELECT * FROM public.user WHERE name={username}")
    rec = list(cursor.fetchall())
    if rec == []:
        cursor.execute(f"INSERT INTO public.user (telegram_id, name) VALUES ({telegram_id}, {username});")
        cursor.execute(f"SELECT * FROM public.user WHERE name={username}")
        rec = list(cursor.fetchall())
    user_id = rec[0][0]
    cursor.execute(f"SELECT * FROM public.role WHERE name=admin")
    rec = list(cursor.fetchall())
    role_id = rec[0][0]
    cursor.execute(f"SELECT * FROM public.role_user WHERE user_id={user_id} AND role_id={role_id}")
    rec = list(cursor.fetchall())
    if rec == []:
        cursor.execute(f"INSERT INTO public.role_user (user_id, role_id) VALUES ({user_id}, {role_id});")
    print("Done")

if __name__ == '__main__':
    user = str(input("input username:"))
    password = str(input("input password:"))
    conn = psycopg2.connect(dbname="bot_db", user=user, password=password)
    cursor = conn.cursor()
    response = str(input("Create a database? y/n"))
    if(response == 'y'):
        create_database(user)
    response = str(input("Add an administrator? y/n"))
    if(response == 'y'):
        username = str(input("Input administrator's name:"))
        telegram_id = int(input("Input administrator's telegram_id"))
        insert_admin(username, telegram_id)
        
    
 