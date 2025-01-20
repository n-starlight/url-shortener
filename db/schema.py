from pydantic import BaseModel
from sqlalchemy.orm import  declarative_base, relationship
from sqlalchemy import Column , Integer , String , TIMESTAMP ,ForeignKey ,DATE,Enum
from datetime import datetime
import enum

#Base class for ORM models(mapped classes)
Base=declarative_base()

class TierLevel(enum.Enum):
    HOBBY="hobby"
    ENTERPRISE="enterprise"

#ORM mapped classes -->
class URL_SHORTENER(Base):
    __tablename__="url_shortener"
    id=Column(Integer,primary_key=True,autoincrement=True)
    original_url=Column(String,nullable=False)
    short_code=Column(String,nullable=False,unique=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    visit_cnt = Column(Integer,default=0,nullable=False)
    last_accessed_at=Column(TIMESTAMP,nullable=True)
    user_id = Column(Integer, ForeignKey("userss.id"),nullable=True)
    deleted_at=Column(TIMESTAMP,nullable=True)
    expiry_date=Column(DATE,nullable=True)
    password=Column(String(50),nullable=True)

    user = relationship("Users", back_populates="urls")

    def __repr__(self)->str:
        return f"""URL_SHORTENER(id : {self.id},original_url:{self.original_url},short_code:{self.short_code},
        visit_cnt:{self.visit_cnt},last_accessed_at:{self.last_accessed_at},
        user_id:{self.user_id},deleted_at:{self.deleted_at},expiry_date:{self.expiry_date})"""

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
    created_at=Column(TIMESTAMP,default=datetime.now)
    tier_level=Column(Enum(TierLevel),default=TierLevel.HOBBY,nullable=False)

    def __repr__(self)->str:
        return f"Users(id : {self.id},email:{self.email},name:{self.name},api_key:{self.api_key},created_at:{self.created_at})"
           
        

    urls=relationship("URL_SHORTENER",back_populates="user")



