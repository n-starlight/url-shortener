from pydantic import BaseModel
from sqlalchemy.orm import  declarative_base, relationship
from sqlalchemy import Column , Integer , String , TIMESTAMP ,ForeignKey
from datetime import datetime

#Base class for ORM models(mapped classes)
Base=declarative_base()

#ORM mapped classes -->
class URL_SHORTENER(Base):
    __tablename__="url_shortener"
    id=Column(Integer,primary_key=True,autoincrement=True)
    original_url=Column(String,nullable=False)
    short_code=Column(String,nullable=False,unique=True)
    created_at = Column(TIMESTAMP, default=datetime.now())
    visit_cnt = Column(Integer,default=0,nullable=False)
    last_accessed_at=Column(TIMESTAMP,nullable=True)
    user_id = Column(Integer, ForeignKey("userss.id"),nullable=True)
    deleted_at=Column(TIMESTAMP,nullable=True)

    user = relationship("Users", back_populates="urls")

    def to_dict(self):
        """
        method of class url_shortener to ensure response is serialised to json if not done already
        """
   
        return {
            "id" : self.id,
            "original_url":self.original_url,
            "short_url":self.short_code,
            "created_at":self.created_at
        }

class Users(Base):
    __tablename__="userss"
    id=Column(Integer,primary_key=True,autoincrement=True)
    email=Column(String(40),nullable=False,unique=True)
    name=Column(String(20),nullable=True)
    api_key=Column(String(100),nullable=False,unique=True)
    created_at=Column(TIMESTAMP,default=datetime.now())

    urls=relationship("URL_SHORTENER",back_populates="user")



