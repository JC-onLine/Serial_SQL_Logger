from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
 
 
from sqlalchemy import create_engine
engine = create_engine('sqlite:///')
 
from sqlalchemy.orm import sessionmaker
 
# Construct a sessionmaker object
session = sessionmaker()
 
# Bind the sessionmaker to engine
session.configure(bind=engine)
 
# Create all the tables in the database which are
# defined by Base's subclasses such as User
Base.metadata.create_all(engine)
