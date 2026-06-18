#!/usr/bin/python3
"""Unit tests for the State class"""
import os
import unittest
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Tests for the State class"""

    def test_is_subclass(self):
        """State inherits from BaseModel"""
        s = State()
        self.assertIsInstance(s, BaseModel)

    def test_instantiation(self):
        """State can be instantiated"""
        s = State()
        self.assertIsNotNone(s.id)

    def test_to_dict_no_sa_state(self):
        """to_dict does not contain _sa_instance_state"""
        s = State()
        d = s.to_dict()
        self.assertNotIn('_sa_instance_state', d)
        self.assertEqual(d['__class__'], 'State')

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage attribute test only'
    )
    def test_name_attribute(self):
        """name is a class attribute in FileStorage mode"""
        self.assertIn('name', State.__dict__)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db',
        'DBStorage attribute test only'
    )
    def test_name_column(self):
        """name is a SQLAlchemy Column in DBStorage mode"""
        from sqlalchemy import Column
        self.assertIn('name', State.__table__.columns.keys())
