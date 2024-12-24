from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession ,async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv
from typing import AsyncGenerator


load_dotenv()

# logging.basicConfig(level=logging.INFO)  # You can change the level to INFO, WARNING, etc.
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# DATABASE_URL format : "postgresql://user:password@localhost/URL_SHORTENER"

#Create async database engine
try:
    engine = create_async_engine(DATABASE_URL,future=True, echo=True)
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

#create an async session factory using engine for connection
async_session=async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)



# Dependency to get database session
#Scope of this will be to a specific route for a single specific request ,new session for each concurrent request when passed as dependency and using proper context scope.
async def get_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:  # using with context manager opens the session on first execute and closes the async session (sesion) instance at the end of with block
        yield session
    # await engine.dispose()  


# Verbose explaination of how it will be used via dep.
# session_generator = get_session()
# session = await session_generator.__anext__()  async session instance 
# Use the session for database operations

          
        
