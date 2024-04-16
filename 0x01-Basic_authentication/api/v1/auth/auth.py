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
        Checks if user is authenticated
        :param path: path to check
        :param excluded_paths: list of paths to exclude
        :return: True if user is authenticated, False otherwise
        """
        return False
    

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