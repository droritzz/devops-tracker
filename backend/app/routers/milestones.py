from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(prefix="/milestones", tags=["Milestones"])

@router.post("/", response_model=schemas.MilestoneResponse)
def create_milestone(milestone: schemas.MilestoneCreate, db: Session = Depends(database.get_db)):
    db_milestone = models.Milestone(**milestone.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.get("/", response_model=list[schemas.MilestoneResponse])
def list_milestones(db: Session = Depends(database.get_db)):
    return db.query(models.Milestone).all()
