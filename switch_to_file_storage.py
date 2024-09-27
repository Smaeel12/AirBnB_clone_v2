#!/usr/bin/python3
from models.user import User
from models.engine import file_storage
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.base_model import BaseModel


class Base():
    pass


storage = file_storage.FileStorage()
storage.reload()
