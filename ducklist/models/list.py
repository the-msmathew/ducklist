from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from .task import Task

class TaskList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    tasks: list["Task"] = Relationship(
        back_populates="list",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
