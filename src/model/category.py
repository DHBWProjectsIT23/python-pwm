from src.crypto.placeholder import dummy_encrypt_fernet, dummy_decrypt_fernet
from typing import NewType
import pickle

Category = NewType("Category", str)


class CategoryList(list[Category]):
    pass
