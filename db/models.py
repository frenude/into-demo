from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase, Session, declared_attr, MappedAsDataclass
from sqlalchemy.sql import func


class BaseMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True, index=True)
    create_time: DateTime = Column(DateTime, default=datetime.now(), unique=True)
    update_time: DateTime = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), unique=True)
    is_delete: bool = Column(Integer, default=0)


class Base(DeclarativeBase, MappedAsDataclass):
    pass


class User(Base, BaseMixin):
    __tablename__ = "users"

    uid: str = Column(String(255), index=True)
    username: str = Column(String(255))
    password: str = Column(String(255))
    avatar: str = Column(String(255))
    nickname: str = Column(String(20))
    bio: str = Column(String(200))
    mobile: str = Column(String(11))
    country: str = Column(Integer)
    regist_time: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    regist_ip: str = Column(String(20))
    login_time: DateTime = Column(DateTime(timezone=True), onupdate=func.now())
    login_ip: str = Column(String(20))

    def __repr__(self):
        return "{}".format(self.__tablename__)

    def dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "username": self.username,
            "password": self.password,
            "avatar": self.avatar,
            "nickname": self.nickname,
            "bio": self.bio,
            "mobile": self.mobile,
            "country": self.country
        }


class Relation(Base, BaseMixin):
    __tablename__ = "relation"
    owner_id: int = Column(Integer)
    another_id: int = Column(Integer)
    type: int = Column(Integer)
    note: str = Column(String(20))
    describe: str = Column(String(200))
