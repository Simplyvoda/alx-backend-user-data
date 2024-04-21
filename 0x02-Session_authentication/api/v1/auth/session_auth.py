#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session authentication class
    """
    user_id_by_session_id = {}


    def create_session(self, user_id: str = None) -> str:
        """
        create a session id for a user with user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())

        user_id = self.user_id_by_session_id[session_id]
        return session_id
    

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        
        return self.user_id_by_session_id.get(session_id)