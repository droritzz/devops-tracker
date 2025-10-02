from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum

class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

# USERS
class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None

class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    name: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

# PROJECTS
class ProjectCreate(BaseModel):
    user_id: uuid.UUID
    name: str
    description: Optional[str] = None

class ProjectOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

# MILESTONES
class MilestoneCreate(BaseModel):
    project_id: uuid.UUID
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class MilestoneUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[StatusEnum]
    due_date: Optional[datetime]

class MilestoneOut(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    description: Optional[str]
    status: StatusEnum
    created_at: datetime
    due_date: Optional[datetime]

    class Config:
        orm_mode = True
