#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class representation """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City",
            cascade="all, delete, delete-orphan",
            backref="state")

    else:
        name = ""
        @property
        def cities(self):
            """ returns all cities with state_id == State.id """

            import models

            list_cities = []
            for key, obj in models.storage.all().items():
                if "City" in key:
                    if obj.state_id == self.id:
                        list_cities += [obj]

            return list_cities
