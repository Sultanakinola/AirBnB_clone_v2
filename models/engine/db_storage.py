#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

import os

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
        # is_test = os.getenv("HBNB_ENV")

        self.__engine = None
        self.__engine = create_engine("{}+{}://{}:{}@{}/{}".format(
            dialect, driver, user, password, host, database),
            pool_pre_ping=True)

        # eng = self.__engine
        # Session = sessionmaker(bind=eng)
        # session = Session()
        # metadata = MetaData()
        # metadata.bind = eng
        # metadata.reflect(bind=eng)

        # tables = metadata.tables
        # try:
        #     tables = [
        #             'amenities',
        #             'cities',
        #             'places',
        #             'reviews',
        #             'states',
        #             'users'
        #         ]
        #     for table in tables:
        #         alt = "ALTER TABLE"
        #         md = "MODIFY"
        #         statements = [
        #             "{} {} {} id varchar(60) FIRST;".format(
        #                 alt,
        #                 table,
        #                 md),
        #             "{} {} {} updated_at datetime after id;".format(
        #                 alt,
        #                 table,
        #                 md),
        #             "{} {} {} created_at datetime after updated_at;".format(
        #                 alt,
        #                 table,
        #                 md)
        #             ]
        #         for statement in statements:
        #             session.execute(text(statement))
        #             session.commit()
        # except Exception:
        #     pass

        # session.close()

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        def all(self, cls=None):
            if cls is not None:
                if type(cls) is str:
                    cls = eval(cls)
                qry = self.__session.query(cls)
                self.__objects = {}
                for obj in qry:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    self.__objects[key] = obj
            else:
                for clas in self.classes_list:
                    qry = self.__session.query(clas)
                    for obj in qry:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        self.__objects[key] = obj

            return self.__objects

        def new(self, obj):
            """ Adds an object to the current db session """

            self.__session.add(obj)

        def save(self):
            """ Saves(Commits) the changes to the db """

            self.__session.commit()

        def delete(self, obj=None):
            """ Delete from the current db session """

            if obj is not None:
                self.__session.delete(obj)

        def reload(self):
            """ Reloads the session by creating the tables """

            Base.metadata.create_all(self.__engine)
            ses = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(ses)
            self.__session = Session()

        def close(self):
            """ closes the current session """

            self.__session.close()
                