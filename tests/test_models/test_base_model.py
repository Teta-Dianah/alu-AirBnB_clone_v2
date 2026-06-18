#!/usr/bin/python3
"""Unit tests for the BaseModel class"""
import os
import unittest
import datetime
from uuid import UUID
import json
from models.base_model import BaseModel


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db',
    'FileStorage tests only'
)
class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel with FileStorage"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def tearDown(self):
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """Test default instantiation"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test instantiation from kwargs does not return same object"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test that integer key in kwargs raises TypeError"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_kwargs_one(self):
        """Test partial kwargs sets attribute and generates missing fields"""
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.Name, 'test')
        self.assertIsNotNone(new.id)
        self.assertIsInstance(new.created_at, datetime.datetime)

    def test_save(self):
        """Test that save persists instance to file"""
        i = self.value()
        i.save()
        key = self.name + '.' + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test string representation format"""
        i = self.value()
        d = {k: v for k, v in i.__dict__.items()
             if k != '_sa_instance_state'}
        self.assertEqual(
            str(i), '[{}] ({}) {}'.format(self.name, i.id, d)
        )

    def test_todict(self):
        """Test to_dict returns correct dictionary"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Test that None kwargs raises TypeError"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """Test that id is a string"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Test that created_at is a datetime"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """Test that updated_at is a datetime"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)

    def test_datetime_attributes(self):
        """Test that two BaseModel instances have different datetime objects"""
        import time
        i = self.value()
        time.sleep(0.001)
        j = self.value()
        self.assertNotEqual(i.created_at, j.created_at)

    def test_uuid(self):
        """Test that id is a valid UUID"""
        new = self.value()
        try:
            UUID(new.id)
        except ValueError:
            self.fail('id is not a valid UUID')

    def test_to_dict_contains_class(self):
        """Test that to_dict contains __class__ key"""
        i = self.value()
        self.assertIn('__class__', i.to_dict())

    def test_to_dict_no_sa_state(self):
        """to_dict does not include _sa_instance_state"""
        i = self.value()
        self.assertNotIn('_sa_instance_state', i.to_dict())

    def test_delete(self):
        """Test that delete removes from storage"""
        from models import storage
        i = self.value()
        i.save()
        key = '{}.{}'.format(self.name, i.id)
        self.assertIn(key, storage.all())
        i.delete()
        self.assertNotIn(key, storage.all())
