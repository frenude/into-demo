from pydantic import BaseModel


class Http(BaseModel):
    host: str = "localhost"
    port: int = "8000"


class DB(BaseModel):
    host: str
    port: int
    user: str
    password: str
    charset: str
    data_base: str
    echo: bool
    pool_size: int
    max_conn: int
    pool_recycle: int
    time_zone: str = "Asia/Shanghai"
    is_postgres: bool = True


class Config(BaseModel):
    http: Http
    db: DB
