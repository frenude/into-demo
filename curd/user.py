import uuid

from sqlalchemy.orm import Session

from db import models
from dto import schemas
from utils import encrypt


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id, models.User.is_delete == 0).first()


def get_user_by_uid(db: Session, uid: str):
    return db.query(models.User).filter(models.User.uid == uid, models.User.is_delete == 0).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_delete == 0).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    fake_hashed_password = ""
    if user.password:
        fake_hashed_password = encrypt.encrypt_passwd(user.password)
    if user.uid is None:
        user.uid = uuid.uuid4()
    if user.nickname is None:
        user.nickname = f"nike-name-{str(user.uid)[:8]}"
    db_user = models.User(uid=user.uid, username=user.username, password=fake_hashed_password, nickname=user.nickname,
                          mobile=user.mobile, regist_ip=user.regist_ip)
    if user.country:
        db_user.country = user.country
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.User(**db_user.dict())


def update_user(db: Session, user: schemas.User) -> schemas.User:
    db_user = db.query(models.User).filter(models.User.id == user.id, models.User.is_delete == 0).first()
    if user.nickname:
        db_user.nickname = user.nickname
    if user.country:
        db_user.country = user.country
    if user.mobile:
        db_user.mobile = user.mobile
    if user.bio:
        db_user.bio = user.bio
    if user.avatar:
        db_user.avatar = user.avatar
    if user.login_ip:
        db_user.login_ip = user.login_ip
    db.commit()
    return db_user


def delete_user_by_id(db: Session, id: int) -> bool:
    ret = db.query(models.User).filter(models.User.id == id).update({'is_delete': 1})
    db.commit()
    return True if ret else False


def delete_user_by_uid(db: Session, uid: str) -> bool:
    ret = db.query(models.User).filter(models.User.uid == uid).update({'is_delete': 1})
    db.commit()
    return True if ret else False
