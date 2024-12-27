from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession ,async_sessionmaker,AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from fastapi import FastAPI
from fastapi import Depends
from contextlib import asynccontextmanager


load_dotenv()

# logging.basicConfig(level=logging.INFO)  # You can change the level to INFO, WARNING, etc.
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# DATABASE_URL format : "postgresql://user:password@localhost/URL_SHORTENER"



@asynccontextmanager
async def app_lifespan(app:FastAPI):
     #Create async database engine
     async_engine=create_async_engine(DATABASE_URL,future=True, echo=True)
     #create an async session factory using engine for connection
     async_session=async_sessionmaker(bind=async_engine,class_=AsyncSession,expire_on_commit=False)

     app.state.engine=async_engine
     app.state.async_session=async_session
     yield

     await async_engine.dispose()


def create_app() -> FastAPI:
    app= FastAPI(lifespan=app_lifespan)
    return app








# try:
#     engine = AsyncEngine(create_engine(DATABASE_URL,future=True, echo=True))
# except Exception as e:
#     print(f"Error connecting to the database: {e}")
#     exit(1)

# async def init_engine():
#      async with engine.connect() as conn:
#           print('connected')
     




# async_session=async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)








          
        
