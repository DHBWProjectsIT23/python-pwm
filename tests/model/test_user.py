# pylint: disable=C

import unittest

from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.user import User


class TestUser(unittest.TestCase):
    def test_init_user(self):
        """
        Test the initialization of a User instance with a hashed username and a Password object.
        """
        user_password = Password("test")
        username = hash_sha256(b"test")
        user = User(username, user_password)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, hash_sha256(b"test"))
        self.assertEqual(user.password(), hash_sha256(b"test"))

    def test_init_static_user(self):
        """
        Test the static method `User.new()` for creating a User instance.
        """
        user = User.new("test", "test")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, hash_sha256(b"test"))
        self.assertEqual(user.password(), hash_sha256(b"test"))
