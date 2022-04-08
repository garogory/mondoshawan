from . import db
from .models import Entry
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))

#def init_db():
#    # import all modules here that might define models so that
#    # they will be registered properly on the metadata.  Otherwise
#    # you will have to import them first before calling init_db()
#    Base.metadata.create_all(bind=engine)


def add_new_entry(address, latitude, longitude):
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_entry = Entry(address=adress, latitude=latitude, longitude=longitude)

    # add the new user to the database
    db.session.add(new_entry)
    db.session.commit()

