from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db, Base
from typing import List
from sqlalchemy import func

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Journey Tracker")
@app.get("/")
def read_root():
    return {"message": "🚀 DevOps Tracker API is running!"}

# ---- Users ----
@app.post("/users/", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(email=payload.email, name=payload.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---- Projects ----
@app.post("/projects/", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # simple validate user exists
    user = db.query(models.User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    project = models.Project(user_id=payload.user_id, name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@app.get("/users/{user_id}/projects", response_model=List[schemas.ProjectOut])
def list_projects(user_id: str, db: Session = Depends(get_db)):
    projects = db.query(models.Project).filter(models.Project.user_id == user_id).all()
    return projects

# progress percentage for a project
@app.get("/projects/{project_id}/progress")
def project_progress(project_id: str, db: Session = Depends(get_db)):
    total = db.query(func.count(models.Milestone.id)).filter(models.Milestone.project_id == project_id).scalar()
    done = db.query(func.count(models.Milestone.id)).filter(models.Milestone.project_id == project_id, models.Milestone.status == models.StatusEnum.done).scalar()
    if total == 0:
        return {"total": 0, "done": 0, "progress_percent": 0}
    percent = (done / total) * 100
    return {"total": total, "done": done, "progress_percent": round(percent, 2)}

# ---- Milestones ----
@app.post("/milestones/", response_model=schemas.MilestoneOut)
def create_milestone(payload: schemas.MilestoneCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).get(payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    m = models.Milestone(
        project_id=payload.project_id,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@app.get("/projects/{project_id}/milestones", response_model=List[schemas.MilestoneOut])
def list_milestones(project_id: str, db: Session = Depends(get_db)):
    ms = db.query(models.Milestone).filter(models.Milestone.project_id == project_id).all()
    return ms

@app.patch("/milestones/{milestone_id}", response_model=schemas.MilestoneOut)
def update_milestone(milestone_id: str, payload: schemas.MilestoneUpdate, db: Session = Depends(get_db)):
    m = db.query(models.Milestone).get(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")
    for field, value in payload:
        if value is not None:
            setattr(m, field, value)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m
