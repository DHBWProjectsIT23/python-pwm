"""
Provides functions for generating SHA-256 and SHA-1 hashes of the given data.
"""

import hashlib


def hash_sha256(data: bytes) -> bytes:
    """
    Generates a SHA-256 hash of the given data.

    Args:
        data (bytes): The data to be hashed. Must be non-empty.

    Returns:
        bytes: The SHA-256 hash of the input data.

    Raises:
        ValueError: If the input data is empty.
    """
    if len(data) == 0:
        raise ValueError("Data to hash is empty")
    return hashlib.sha256(data).digest()


def hash_sha1(data: bytes) -> bytes:
    """
    Generates a SHA-1 hash of the given data.

    Args:
        data (bytes): The data to be hashed. Must be non-empty.

    Returns:
        bytes: The SHA-1 hash of the input data.

    Raises:
        ValueError: If the input data is empty.
    """
    if len(data) == 0:
        raise ValueError("Data to hash is empty")
    return hashlib.sha1(data).digest()
