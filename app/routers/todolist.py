from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import TodoList

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ToDoList 아이템 가져오기
@router.get("/getList")
async def get_todolist(db: Session = Depends(get_db)):
    items = db.query(TodoList).all()
    return {"data": [
        {
            "id": item.id,
            "title": item.title,
            "check_status": item.check_status,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        } for item in items
    ]}

# ToDoList 아이템 추가하기
@router.post("/createList")
async def create_todolist(db: Session = Depends(get_db)):
    try:
        todo = TodoList()
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return {"result": "성공"}
    except Exception as e:
        return {"result": "실패"}


# ToDoList 아이템 수정하기
@router.post("/updateList")
async def update_todolist(item: dict, db: Session = Depends(get_db)):
    return {'수정하기'}


# ToDoList 아이템 삭제하기
@router.post("/deleteList")
async def delete_todolist(item: dict, db: Session = Depends(get_db)):
    return {'삭제하기'}