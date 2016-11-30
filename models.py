from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from passlib.apps import custom_app_context as pwd_context
import datetime
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password_hash = Column(String(64))
    email = Column(String(64))
    #----------------------------------------------------------------------
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

# create tables

class Weburl(Base):

    __tablename__ = "urls"

    id = Column(Integer, primary_key= True)
    original_url = Column(String(300))
    shortened_url = Column(String(40))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    no_of_click = Column(Integer, default=0)
    visits_in_chrome = Column(Integer, default=0)
    visits_in_firefox = Column(Integer, default=0)
    visits_in_safari = Column(Integer, default=0)
    visits_in_internet_explorer = Column(Integer, default=0)
    visits_in_android = Column(Integer, default=0)
    visits_in_ios = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(User)



Base.metadata.create_all(engine)