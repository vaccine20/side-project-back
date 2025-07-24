from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(
    title='저는 김선용 입니다.',
    description='토이 프로젝트로 간단히 하나 만들어보았습니다.',
    version='1.0'
)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ['GET', 'POST'],
    allow_headers = ['Authorization']
)

@app.get('/init')
async def root():
    return 'api 통신에 성공하였습니다.'

@app.get('/items/{user_id}')
async def read_item(user_id: str, user_name: Optional[str] = None):
    if user_name:
        return {
            'data' : user_name + ' = ' + user_id
        }
    
    return {
        'data' : user_id + ' = ' + '누구세요?'
    }