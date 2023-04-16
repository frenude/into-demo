from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declared_attr
from conf import cfg

SQLALCHEMY_DATABASE_URL = ""
if cfg.db.is_postgres:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{cfg.db.user}:{cfg.db.password}@{cfg.db.host}:{cfg.db.port}/{cfg.db.data_base}?charset={cfg.db.charset}"
else:
    SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{cfg.db.user}:{cfg.db.password}@{cfg.db.host}:{cfg.db.port}/{cfg.db.data_base}?charset={cfg.db.charset}'

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       echo=cfg.db.echo,
                       pool_size=cfg.db.pool_size,
                       max_overflow=cfg.db.max_conn,
                       pool_recycle=cfg.db.pool_recycle)

SessionLocal = sessionmaker(bind=engine)
