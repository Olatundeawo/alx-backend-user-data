#!/usr/bin/env python3
"""
Database module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Save the user to the database
        """

        add_user = User(email=email, hashed_password=hashed_password)
        self._session.add(add_user)
        self._session.commit()

        return add_user

    def find_user_by(self, **kwarg) -> User:
        """
        method that query the database
        """
        if kwarg is None:
            raise InvalidRequestError

        column_name = User.__table__.columns.keys()
        for key in kwarg.keys():
            if key not in column_name:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwarg).one()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update the user attribute
        """
        user = self.find_user_by(id=user_id)

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()