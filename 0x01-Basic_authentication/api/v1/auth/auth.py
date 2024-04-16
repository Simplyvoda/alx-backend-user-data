#!/usr/bin/env python3
"""Authentication module for the API.
"""
import re
from flask import request
from typing import List, TypeVar

class Auth():
    """
    Auth class
    """
    def __init__(self):
        """
        Initialise class
        """
        pass


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if path requires authentication
        :param path: path to check
        :param excluded_paths: list of paths to exclude
        :return: True if user is authenticated, False otherwise
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True
    

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header from the request
        :param request: request object
        :return: Authorization header
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current authenticated user
        :param request: request object
        :return: current authenticated user
        """
        return None