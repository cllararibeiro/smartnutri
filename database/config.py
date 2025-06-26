from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

engine = create_engine('mysql+pymysql://root:@localhost:3307/db_smartnutri')
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass