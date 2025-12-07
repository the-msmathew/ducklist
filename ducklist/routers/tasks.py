from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from ducklist.models.task import Task
from ducklist.db import get_session

route = APIRouter(
    prefix="/lists/{list_id}/tasks",
    tags=["tasks"]
)

@route.post("/")
def create_task(list_id: int, task_data: Task, session: Session = Depends(get_session)):
    task_data.list_id = list_id

    # Not doing much validating on frontend right now
    if isinstance(task_data.due_date, str):
        task_data.due_date = datetime.fromisoformat(task_data.due_date)

    session.add(task_data)
    session.commit()
    session.refresh(task_data)
    return task_data

@route.get("/")
def get_tasks(list_id: int, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.list_id == list_id)).all()
    return tasks

@route.put("/{task_id}")
def update_task(list_id: int, task_id: int, task_data: Task, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.list_id != list_id:
        raise HTTPException(status_code=404, detail="Task not found")

    if "due_date" in task_data.dict(exclude_unset=True):
        if isinstance(task_data.due_date, str):
            task_data.due_date = datetime.fromisoformat(task_data.due_date)

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@route.delete("/{task_id}")
def delete_task(list_id: int, task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.list_id != list_id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
