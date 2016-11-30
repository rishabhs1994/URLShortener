import pyperclip

def g():
	pyperclip.copy('The text to be copied to the clipboard.')
if(__name__ == '__main__'):
	g()



"""
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

link1 = Weburl(original_url="First", shortened_url="First", user_id="0")
session.add(link1)
link2 = Weburl(original_url="F", shortened_url="f", user_id="1")
session.add(link2)

link3 = Weburl(original_url="G", shortened_url="g", user_id="1")
session.add(link3)

link4 = Weburl(original_url="H", shortened_url="h", user_id="2")
session.add(link4)
# commit the record the database
session.commit()
 
session.commit()
"""