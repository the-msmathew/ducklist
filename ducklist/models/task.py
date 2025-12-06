from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
    due_date: datetime
    location: Optional[str] = None

    list_id: Optional[int] = Field(default=None, foreign_key="tasklist.id")
    list: "TaskList" = Relationship(back_populates="tasks")
