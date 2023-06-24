#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone
using SQLAlchemy"""

import os
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine, MetaData, Table, Column, String, text
from sqlalchemy.orm import sessionmaker, scoped_session

class_names = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class DBStorage:
    """This class manages storage of hbnb models in JSON format"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the storage class"""

        dialect = "mysql"
        driver = "mysqldb"
        user = os.getenv("HBNB_MYSQL_USER", default="hbnb_dev")
        password = os.getenv("HBNB_MYSQL_PWD", default="hbnb_dev_pwd")
        host = os.getenv("HBNB_MYSQL_HOST", default="localhost")
        database = os.getenv("HBNB_MYSQL_DB", default="hbnb_dev_db")
        self.__engine = create_engine("{}+{}://{}:{}@{}/{}".format(
            dialect, driver, user, password, host, database),
            pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the current database session """
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = class_names.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in class_names.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def new(self, obj):
        """ Adds an object to the current database session """

        self.__session.add(obj)

    def save(self):
        """ Saves(Commits) the changes to the database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if not self.__session:
            self.reload()
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Reloads the session by creating the tables """

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
            )
        self.__session = scoped_session(session_factory)

    def close(self):
        """ closes the current session """
        self.__session.close()
