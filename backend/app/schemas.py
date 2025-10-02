from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

# ---------- User ----------
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password_hash: str

class UserResponse(UserBase):
    id: uuid.UUID
    class Config:
        orm_mode = True

# ---------- Project ----------
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    user_id: uuid.UUID

class ProjectResponse(ProjectBase):
    id: uuid.UUID
    class Config:
        orm_mode = True

# ---------- Milestone ----------
class MilestoneBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str

class MilestoneCreate(MilestoneBase):
    project_id: uuid.UUID

class MilestoneResponse(MilestoneBase):
    id: uuid.UUID
    class Config:
        orm_mode = True
