from database.models import *
from sqlalchemy import create_engine


db = create_engine("sqlite+pysqlite:///database__")
Base.metadata.create_all(db)
