from fastapi import FastAPI
from fastapi.responses import Response
import uvicorn
import asyncio
from db import SessionLocal, User


users = []


async def saver_every_minute():
    print('start func')
    while True:
        print('start minute...')
        await asyncio.sleep(60)
        db = SessionLocal()
        users_to_save = [User(name=user['name'], age=user['age']) for user in users]
        db.bulk_save_objects(users_to_save)
        db.commit()
        print(f'save objects {users_to_save}')
        users.clear()


app = FastAPI()


@app.post('/')
async def user_endpoint(name: str, age: int):
    if age < 18:
        return Response(content='age is lower then 18')
    
    users.append({'name': name, 'age': age})
    print(users)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(saver_every_minute())



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000),
