from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

class User(Base, SerializerMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

class Wine(Base, SerializerMixin):
    __tablename__ = 'Wines'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.Text, unique=True)
    year = db.Column(db.BigInteger)
    country = db.Column(db.Text)
    region_1 = db.Column(db.Text)
    designation = db.Column(db.Text)
    variety = db.Column(db.Text)
    description = db.Column(db.Text)
    points = db.Column(db.BigInteger)
    price = db.Column(db.Float)
    taster_name = db.Column(db.Text)
    taster_twitter_handle = db.Column(db.Text)

    def __init__(self, title=None):
        self.title = title

# Create tables.
Base.metadata.create_all(bind=engine)
