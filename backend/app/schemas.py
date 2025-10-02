from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    user_id: UUID

class ProjectResponse(ProjectBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- Milestone Schemas ---
class MilestoneBase(BaseModel):
    title: str
    description: str | None = None
    status: str | None = None
    due_date: datetime | None = None

class MilestoneCreate(MilestoneBase):
    project_id: UUID  # link to project

class MilestoneResponse(MilestoneBase):
    id: UUID
    project_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
