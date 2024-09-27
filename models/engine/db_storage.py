from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
"""Module for DBstorage class"""


class DBStorage:
    """Class for database storage"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        """Initializes storage"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns all objects of cls"""
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = self.__session.query(
                User, State, City, Amenity, Place, Review).all()
        return {"{}.{}".format(type(obj).__name__, obj.id): obj
                for obj in objs}

    def new(self, obj):
        """add object to db"""
        self.__session.add(obj)

    def save(self):
        """commit changes to db"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from db"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the db"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)
