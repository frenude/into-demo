import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import models
from db.database import SessionLocal, engine
from dto import schemas
from curd import user as curd_user
from conf import cfg

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    s = SessionLocal()
    try:
        yield s
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


@app.post("/users/", response_model=schemas.Response)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.uid:
        db_user = curd_user.get_user_by_uid(db, uid=user.uid)
        if db_user:
            return schemas.Response(code=0, msg="User already created", data=None)
    return schemas.Response(code=1, msg="Create User Success", data=curd_user.create_user(db=db, user=user))


@app.get("/users/", response_model=schemas.Response)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = curd_user.get_users(db, skip=skip, limit=limit)
    return schemas.Response(code=1, msg="Select Users Success", data=users)


@app.get("/users/{id}", response_model=schemas.Response)
def get_user_id(id: int, db: Session = Depends(get_db)):
    users = curd_user.get_user_by_id(db, id=id)
    return schemas.Response(code=1, msg="Select User Success", data=users)


@app.get("/users/{uid}", response_model=schemas.Response)
def get_user_uid(uid: str, db: Session = Depends(get_db)):
    users = curd_user.get_user_by_uid(db, uid=uid)
    return schemas.Response(code=1, msg="Select User Success", data=users)


@app.put("/users/", response_model=schemas.Response)
def update_user(user: schemas.User, db: Session = Depends(get_db)):
    return schemas.Response(code=1, msg="Update User Success", data=curd_user.update_user(db, user))


@app.delete("/users/{id}", response_model=schemas.Response)
def delete_user_id(id: int, db: Session = Depends(get_db)):
    if curd_user.delete_user_by_id(db, id):
        return schemas.Response(code=1, msg="Delete User Success", data=None)
    else:
        return schemas.Response(code=0, msg="Delete User Failed", data=None)


@app.delete("/users/{uid}", response_model=schemas.Response)
def delete_user_id(uid: str, db: Session = Depends(get_db)):
    if curd_user.delete_user_by_uid(db, uid):
        return schemas.Response(code=1, msg="Delete User Success", data=None)
    else:
        return schemas.Response(code=0, msg="Delete User Failed", data=None)


if __name__ == '__main__':
    uvicorn.run(app="main:app", host=cfg.http.host, port=cfg.http.port, reload=True)
