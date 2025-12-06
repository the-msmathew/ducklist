from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ducklist.models.list import TaskList
from ducklist.db import get_session

route = APIRouter(
    prefix="/lists",
    tags=["lists"]
)

@route.post("/")
def create_list(list_data: TaskList, session: Session = Depends(get_session)):
    session.add(list_data)
    session.commit()
    session.refresh(list_data)
    return list_data

@route.get("/")
def get_lists(session: Session = Depends(get_session)):
    lists = session.exec(select(TaskList)).all()
    return lists

@route.get("/{list_id}")
def get_list(list_id: int, session: Session = Depends(get_session)):
    task_list = session.get(TaskList, list_id)
    if not task_list:
        raise HTTPException(status_code=404, detail="List not found")
    return task_list

@route.delete("/{list_id}")
def delete_list(list_id: int, session: Session = Depends(get_session)):
    task_list = session.get(TaskList, list_id)
    if not task_list:
        raise HTTPException(status_code=404, detail="List not found")
    session.delete(task_list)
    session.commit()
    return {"ok": True}
