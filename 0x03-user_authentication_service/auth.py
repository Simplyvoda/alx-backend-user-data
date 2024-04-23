#!/usr/bin/env python3
"""
Module for Authentication methods
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns salted hash of input password
    """
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pwd
