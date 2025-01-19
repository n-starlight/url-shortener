import secrets,asyncio,os
from backend.main_new import app
from fastapi import HTTPException,Depends
from schema import Users,URL_SHORTENER
from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine,AsyncSession
# from conn_session import create_app
from dotenv import load_dotenv
from sqlalchemy import select,delete,func,update
from fastapi import FastAPI

load_dotenv()



DATABASE_URL = os.getenv("DATABASE_URL")
# async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)
# async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# def create_app() -> FastAPI:
#     app = FastAPI()
#     async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)
#     app.state.async_session = async_sessionmaker(
#         bind=async_engine, class_=AsyncSession, expire_on_commit=False
#     )
#     return app

# app = create_app()


def generate_api_key():
    return secrets.token_urlsafe(32)  # Generates a 43-character base64 string(A-Z,a-z,0-9)


async def create_user(email,name=None,session=None):
    if not session:
        raise ValueError("session not available")
    print('session active')
    api_key=generate_api_key()
    new_user=Users(email=email,name=name,api_key=api_key)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"user_id":new_user.id,"api_key":new_user.api_key}

async def sample_users():
    emails=["reddstar@starescape.com","pinkkstar@starescape.com","yellowwstar@starescape.com","redorangeestar@starescape.com"]
    names=["redstarr","pinkstarr","yellowstarr","redorangestarr"]
    users=[]
    async_session = app.state.async_session
    if async_session is None:
        raise RuntimeError("app.state.async_session is not initialized!")
    async with async_session() as session:
        for email,name in zip(emails,names):
            new_userdata=await create_user(email,name=name,session=session)
            users.append(new_userdata)
    print("users",users)
    return users 

async def get_users():
    async_session = app.state.async_session
    async with async_session() as session:
       stmt=select(Users)
       result=await session.execute(stmt)
    return result.scalars().first()
    

async def main():
    async with app.router.lifespan_context(app):
        # result=await sample_users()
        # print("sample users:",result)
        result=await get_users()
        print("get users: ",result)

if __name__ == "__main__":
    asyncio.run(main())
    print("Sample users seeded successfully!")
    



    