#!/usr/bin/env python3
"""
Authorized module
"""
import re
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ class Module"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        used for authorized request
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
        Header request validation
        """
        if request is None:
            return request.headers.get('Authorization', None)
        return None
    

    def current_user(self, request=None) -> TypeVar("User"):
        """
        update the function soon
        """
        return None


    def session_cookie(self, request = None) -> int:
        """
        returns a cookie value from a request
        """
        if request:
            SESSION_NAME = getenv("SESSION_NAME")
            if SESSION_NAME:
                value = request.cookies.get(SESSION_NAME)
                return value
            else:
                return None
        else:
            return None