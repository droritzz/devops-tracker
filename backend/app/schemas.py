from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Users
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Projects
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Milestones
class MilestoneBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None

class MilestoneCreate(MilestoneBase):
    pass

class MilestoneResponse(MilestoneBase):
    id: int
    status: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
