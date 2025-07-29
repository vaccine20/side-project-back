from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.db import SessionLocal
from app.models import TodoList, get_kst_now

router = APIRouter()

# 데이터베이스
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# pydantic 모델 정의
# 데이터 타입 검증과 변환을 위해 사용
class TodoCreate(BaseModel):
    id: str
    title: str
    check_status: Optional[bool] = False

class TodoUpdate(BaseModel):
    id: str
    title: str

class TodoDelete(BaseModel):
    id: str

# ToDoList 아이템 가져오기
@router.get("/getList")
async def get_todolist(db: Session = Depends(get_db)):
    try:
        items = db.query(TodoList).all()
        return [
            {
                "id": item.id,
                "title": str(item.title),
                "check_status": item.check_status,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            } for item in items
        ]
    except:
        return {"result": "실패"}

# ToDoList 아이템 추가하기
@router.post("/createList")
async def create_todolist(item: TodoCreate, db: Session = Depends(get_db)):
    try:
        todo = TodoList(
            id=item.id, 
            title=str(item.title),
            check_status=item.check_status, 
            created_at=get_kst_now(),
            updated_at=get_kst_now()
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return {"result": "성공"}
    except Exception as e:
        db.rollback()
        return {"result": "실패"}


# ToDoList 아이템 수정하기
@router.post("/updateList")
async def update_todolist(item: List[TodoUpdate], db: Session = Depends(get_db)):
    try:
        for i in item:
            update_id = i.id

            if not update_id:
                continue

            update_item = db.query(TodoList).filter(TodoList.id == update_id).first()
            if update_item:
                update_item.title = i.title
                update_item.updated_at = get_kst_now()
        db.commit()
        return {"result": "성공"}
    except:
        db.rollback()
        return {"result": "실패"}


# ToDoList 아이템 삭제하기
@router.post("/deleteList")
async def delete_todolist(item: List[TodoDelete], db: Session = Depends(get_db)):
    try: 
        delete_ids = [i.id for i in item]
        
        if not delete_ids:
            return {"result": "성공"}
        
        db.query(TodoList).filter(TodoList.id.in_(delete_ids)).delete(synchronize_session=False)
        db.commit()
        return {"result": "성공"}
    except:
        db.rollback()
        return {"result": "실패"}