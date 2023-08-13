#!/usr/bin/env python3
"""
session module
"""
from typing import TypeVar
from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    class module
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a session id for user
        """
        if user_id is None:
            return None
        if isinstance(user_id, str) is False:
            return None
        
        id_key = str(uuid.uuid4())
        self.user_id_by_session_id[id_key] = user_id
        
        return id_key
    

    def user_id_for_session_id(self, session_id: str = None) ->str :
        """
        method for retrieving a link between
        user id and session id
        """
        if session_id is None:
            return None
        if isinstance(session_id, str) is False:
            return None
        
        value = self.user_id_by_session_id.get(session_id)

        return value


    def current_user(self, request=None) -> TypeVar("User"):
        """
        using session id to ientify user
        """
        session_id = self.session_cookie(request)

        if session_id is None:
            return None
        
        user_id = self.user_id_by_session_id(session_id)

        return User.get(user_id)
    
    def destroy_session(self, request=None):
        """Deletes de user session / logout"""

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True