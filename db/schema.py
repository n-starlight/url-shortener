from pydantic import BaseModel
from sqlalchemy.orm import  declarative_base
from sqlalchemy import Column , Integer , String , TIMESTAMP 
from datetime import datetime

#Base class for ORM models
Base=declarative_base()

class URL_SHORTENER(Base):
    __tablename__="url_shortener"
    id=Column(Integer,primary_key=True,autoincrement=True)
    original_url=Column(String,nullable=False)
    short_code=Column(String,nullable=False,unique=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    visit_cnt = Column(Integer,default=0,nullable=False)
    last_accessed_at=Column(TIMESTAMP,nullable=True)

    # def to_dict(self):
    #     """
    #     method of class url_shortener to ensure response is serialised to json is not done already
    #     """
   
    #     return {
    #         "id" : self.id,
    #         "original_url":self.original_url,
    #         "short_url":self.short_code,
    #         "created_at":self.created_at
    #     }




