from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ducklist.models.task import Task
from ducklist.db import get_session

route = APIRouter(
    prefix="/lists/{list_id}/tasks",
    tags=["tasks"]
)

@route.post("/")
def create_task(list_id: int, task_data: Task, session: Session = Depends(get_session)):
    task_data.list_id = list_id
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
