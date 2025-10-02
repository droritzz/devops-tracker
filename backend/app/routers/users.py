from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(prefix="/users", tags=["users"])

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET all users
@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# POST create a user
@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=user.password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
