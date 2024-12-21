from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# logging.basicConfig(level=logging.INFO)  # You can change the level to INFO, WARNING, etc.
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# DATABASE_URL format : "postgresql://user:password@localhost/URL_SHORTENER"

#Create database engine

try:
    engine = create_engine(DATABASE_URL, echo=True)
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# try:
#     engine = create_async_engine(DATABASE_URL)
# except Exception as e:
#     print(f"Error connecting to the database: {e}")
#     exit(1)

# Dependency for database connection
async def get_db_connection():
    # conn
    try:
        with engine.connect() as conn:
            logger.info("Wohoo connected !!")
            yield conn #use yield as it will be used as a dependency
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError occurred: {e}")
        raise  # Propagate the error
    except Exception as e:
         # Handle any other unforeseen exceptions
        logger.error(f"Unexpected error occurred: {e}")
        raise  # Re-raise the exception after logging it to propagate errors 

    #comment below while using test_query
    # finally:
    #     if conn:
    #         conn.close()
    #         logger.info("Database connection closed.")



# if __name__ == '__main__':
    # test_query()
get_db_connection()