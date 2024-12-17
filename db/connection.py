from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# logging.basicConfig(level=logging.INFO)  # You can change the level to INFO, WARNING, etc.
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL format : "postgresql://user:password@localhost/URL_SHORTENER"

engine = create_engine(DATABASE_URL, echo=True)

# Dependency for database connection
def get_db_connection():
    conn = None
    try:
        conn = engine.connect()
        logger.info("Wohoo connected !!")
        # return conn
        yield conn
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError occurred: {e}")
        raise  # Propagate the error
    except Exception as e:
         # Handle any other unforeseen exceptions
        logger.error(f"Unexpected error occurred: {e}")
        raise  # Re-raise the exception after logging it to propagate errors 

    #comment below while using test_query
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

# def test_query():
#     query='SELECT COUNT(*) FROM url_shortener'
#     try:
#         with get_db_connection() as conn:
#             result=conn.execute(text(query))
#         row=result.fetchone()
#         print("Query executed successfully.")
#         print("Row:", row)
#     except SQLAlchemyError as e:
#         print(f"SQLAlchemy error executing query: {e}")
#     except Exception as e:
#         print(f"Error executing query: {e}")
#     finally:
#         if conn:
#             conn.close()
#             print("Connection closed.")

# if __name__ == '__main__':
    # test_query()
get_db_connection()