import datetime
import sys
import os


class Metadata:
    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        self.last_accessed_at = datetime.datetime.now()
        self.created_by = os.getlogin()
        self.modified_by = os.getlogin()
        self.last_accessed_by = os.getlogin()

    def accessed(self) -> None:
        self.last_accessed_at = datetime.datetime.now()
        self.last_accessed_by = os.getlogin()

    def modified(self) -> None:
        self.accessed()
        self.modified_at = datetime.datetime.now()
        self.modified_by = os.getlogin()

    def __str__(self) -> str:
        return f"""
Created at: {self.created_at}\nCreated by: {self.created_by}\n
Modified at: {self.modified_at}\nModified by: {self.modified_by}\n
Last accessed at: {self.last_accessed_at}\nLast accessed by: {self.last_accessed_by}
"""
