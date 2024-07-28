from typing import NewType
import pickle
from src.crypto.placeholder import dummy_encrypt_fernet, dummy_decrypt_fernet

Note = NewType("Note", str)


class NoteList(list[Note]):
    pass
