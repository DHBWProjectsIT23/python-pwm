import pickle
import unittest

from src.crypto.placeholder import dummy_decrypt_fernet
from src.model.metadata import EncryptedMetadata
from src.model.metadata import Metadata
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.user import User


class TestPasswordInformation(unittest.TestCase):
    def test_init(self):
        _ = create_test_info()

    def test_note(self):
        info, _, _ = create_test_info()
        note = "This password is a test"
        info.set_note(note)
        self.assertEqual(info.details.note, note.encode())

    def test_category_maximum(self):
        info, _, _ = create_test_info()
        categories = ["Test", "Old", "Password"]
        info.add_categories(categories)
        more_categories = ["AnotherTest"], ["Safe"], ["Uncool"]
        self.assertRaises(ValueError, info.add_categories, more_categories)
        info.add_category("AnotherTest")
        info.add_category("Safe")
        self.assertRaises(ValueError, info.add_category, "Uncool")

    def test_duplicate_category(self):
        info, _, _ = create_test_info()
        info.add_category("Test")
        self.assertRaises(ValueError, info.add_category, "Test")

    def test_encrypt(self):
        info, _, _ = create_test_info()
        info.add_password(Password("test2"))
        for password in info.passwords:
            self.assertFalse(password.is_encrypted)
        self.assertIsInstance(info.metadata, Metadata)

        info.encrypt_data(user_password="FakeKey")
        info.encrypt_passwords(user_password="FakeKey")
        for password in info.passwords:
            self.assertTrue(password.is_encrypted)
        self.assertIsInstance(info.metadata, EncryptedMetadata)

    def test_decrypt(self):
        info, _, _ = create_test_info()

        info.add_password(Password("test2"))
        info.encrypt_data(user_password="FakeKey")
        info.encrypt_passwords(user_password="FakeKey")
        for password in info.passwords:
            self.assertTrue(password.is_encrypted)
        self.assertIsInstance(info.metadata, EncryptedMetadata)

        info.decrypt_data(user_password="FakeKey")
        info.decrypt_passwords(user_password="FakeKey")
        for password in info.passwords:
            self.assertFalse(password.is_encrypted)
        self.assertIsInstance(info.metadata, Metadata)


def create_test_info() -> tuple[PasswordInformation, Password, User]:
    test_password = Password("test")
    test_user = User.new("test_user", "test_user_pw")
    test_info = PasswordInformation(test_user, test_password, "Test Password")
    return test_info, test_password, test_user
