from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from zoneinfo import ZoneInfo

Base = declarative_base()

def get_kst_now():
    return datetime.datetime.now(ZoneInfo("Asia/Seoul"))

class TodoList(Base):
    __tablename__ = "todo_list"
    id = Column(String(64), primary_key=True, index=True)
    title = Column(String, default="")
    check_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_kst_now)
    updated_at = Column(DateTime, default=get_kst_now, onupdate=get_kst_now)
