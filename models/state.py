#!/usr/bin/python3
"""This module defines the State class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represents a state."""

    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City',
            backref='state',
            cascade='all, delete-orphan'
        )
    else:
        name = ""

        @property
        def cities(self):
            """Return all City objects whose state_id matches this state."""
            from models import storage
            from models.city import City
            return [
                c for c in storage.all(City).values()
                if c.state_id == self.id
            ]
