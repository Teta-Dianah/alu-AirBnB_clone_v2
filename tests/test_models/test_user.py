#!/usr/bin/python3
"""Unit tests for the User class"""
import os
import unittest
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Tests for the User class"""

    def test_is_subclass(self):
        """User inherits from BaseModel"""
        u = User()
        self.assertIsInstance(u, BaseModel)

    def test_instantiation(self):
        """User can be instantiated"""
        u = User()
        self.assertIsNotNone(u.id)

    def test_to_dict_no_sa_state(self):
        """to_dict does not contain _sa_instance_state"""
        u = User()
        d = u.to_dict()
        self.assertNotIn('_sa_instance_state', d)
        self.assertEqual(d['__class__'], 'User')

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage attribute test only'
    )
    def test_class_attributes(self):
        """email, password, first_name, last_name are class attributes"""
        for attr in ['email', 'password', 'first_name', 'last_name']:
            self.assertIn(attr, User.__dict__)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db',
        'DBStorage tests only'
    )
    def test_db_columns(self):
        """User has required DB columns"""
        cols = User.__table__.columns.keys()
        for col in ['email', 'password']:
            self.assertIn(col, cols)
