#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
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
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        Adds a new user
        Returns: User Object
        """
        new_user = User(email=email, hashed_password=hashed_password)

        self._session.add(new_user)

        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user based on keyworded arguments
        Returns: User Object
        """
        fields, values = [], []
        for k, v in kwargs.items():
            if hasattr(User, k):
                fields.append(getattr(User, k))
                values.append(v)
            else:
                raise InvalidRequestError()
        res = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if res is None:
            raise NoResultFound()
        return res

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Finds a user in the db and updates the user according
        """
        user = self.find_user_by(id=user_id)
        if user is not None:
            new_value = {}
            for k, v in kwargs.items():
                if hasattr(User, k):
                    new_value[getattr(User, k)] = v
                else:
                    raise ValueError()
            self._session.query(User).filter(User.id == user_id).update(
                new_value,
                synchronize_session=False,
            )
            self._session.commit()
