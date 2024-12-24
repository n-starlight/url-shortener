from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException,Depends
import hashlib
from typing import Union
from sqlalchemy import select,delete
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import  AsyncSession

from db.conn_session import get_session
from db.schema import URL_SHORTENER

load_dotenv()


app = FastAPI()

class LongUrl(BaseModel):
    url_link:str
    custom_slug:Union[str, None] = None

DOMAIN="https://heystarlette/"



 
# @app.get("/")
# def read_root():
#     return {"Url shortener active"}

async def check_code_exists(session,short_code:str):
    result = await session.execute(
       select(URL_SHORTENER.original_url,URL_SHORTENER.short_code).where(URL_SHORTENER.short_code==short_code)
    )
    # new_res=result.scalars()
    # print(result)
    # print("first",result.first())
    # print("all",result.all())
    # print("curr",result.first())
    return result.first()


async def retry_ifnot_unq(short_code:str,url,session):
    
    max_attempts = 5
    attempts = 0
    while True:
        hash_code_new = hashlib.md5(f"{url}{attempts}".encode()).hexdigest()[:6]
        code_exists=await check_code_exists(session,hash_code_new) 
        code_exists_scode=code_exists.URL_SHORTENER.short_code if code_exists else None 
        if not code_exists_scode:
            break
        attempts+=1

       

        if attempts>=max_attempts:
            raise HTTPException(status_code=500,detail='couldn''t generate unique code')
        
        
    short_code=hash_code_new
    return short_code

async def save_url(session,original_url:str,short_code:str):
    new_url=URL_SHORTENER(original_url=original_url,short_code=short_code)
    session.add(new_url)
    try:
        await session.commit()
        await session.refresh(new_url)
        return new_url
    except IntegrityError:
        await session.rollback()
        # return new_url   #can return directly without below checks if there was no hash collision issue with  different users different payloads , hash code not already existing in db 
        code_exists=await check_code_exists(session,short_code)
        code_exists_url=code_exists.original_url if code_exists else None
        code_exists_scode=code_exists.short_code if code_exists else None
        if code_exists_scode:
            if code_exists_url==original_url:
               return new_url
            else:
               short_code=await retry_ifnot_unq(short_code,original_url,session)
               newinsert= await save_url(session,original_url,short_code)
               return newinsert
        
        
    

async def get_url(short_code,session):
   
        result = await session.execute(
           select(URL_SHORTENER.original_url).where(URL_SHORTENER.short_code==short_code)
        )
        fetchresult=result.first()
        return fetchresult if fetchresult else None

    


# def shorten_url(payload:LongUrl,db_conn=Depends(get_db_connection)):  
#     short_code=payload.custom_slug
#     if short_code:
#         if check_code_exists(db_conn,short_code):
#             raise HTTPException(status_code=500,detail='Please enter a unique code ,it already exists')
    
#     else:
#         hash_code=hashlib.md5(payload.url_link.encode()).hexdigest()[:6]
#         print("hash-code",hash_code)
#         short_code=retry_ifnot_unq(hash_code,payload,db_conn)
    
#     newinsert= save_url(db_conn,original_url=payload.url_link,short_code=short_code)
#     print('newinsert',newinsert)
#     response={"short_url":f"{DOMAIN}{newinsert[2]}"}
#     return response

@app.post("/shorten")
async def shorten_url(payload:LongUrl,db_session:AsyncSession=Depends(get_session)): 
   
    hash_code=hashlib.md5(payload.url_link.encode()).hexdigest()[:6]
    code_exists=await check_code_exists(db_session,hash_code)
    code_exists_url=code_exists.original_url if code_exists else None
    code_exists_scode=code_exists.short_code if code_exists else None
    
    if code_exists_scode:
        if code_exists_url==payload.url_link:
            short_code=hash_code
            response={"short_url":f"{short_code}"}
        else:
            short_code=await retry_ifnot_unq(hash_code,payload.url_link,db_session)
            newinsert= await save_url(db_session,original_url=payload.url_link,short_code=short_code)
            print('newinsert',newinsert)
            response={"short_url":f"{newinsert.short_code}"}
            
    else:
        short_code=hash_code
        newinsert=await save_url(db_session,original_url=payload.url_link,short_code=short_code)
        print('newinsert',newinsert)
        response={"short_url":f"{newinsert.short_code}"}
    
    return response




@app.get("/redirect")
async def redirect_url(short_code:str,db_session:AsyncSession=Depends(get_session)):
    url= await get_url(short_code,db_session)

    if not url:
       raise HTTPException(status_code=404, detail="URL not found")
    print("url",url)
    return RedirectResponse(url=url.original_url,status_code=307)
    # response = {"original_url": url}
    # return response

async def del_scode(session,short_code):
    await session.execute(delete(URL_SHORTENER).where(URL_SHORTENER.short_code==short_code))
    await session.commit()
    


@app.delete("/shorten/{short_code}")
async def remove_scode(short_code:str,db_session:AsyncSession=Depends(get_session)):
    code_exists=await check_code_exists(db_session,short_code) 

    if code_exists:
        await del_scode(db_session,short_code)
        return {"message": f"{short_code} short code has been deleted"}
    else:
        raise HTTPException(status_code=404,detail="Not a valid short code")


# Handling of race conditions --
#A race condition occurs when two or more processes or threads attempt to perform an operation on shared resources simultaneously in such a way 
# that the outcome depends on the timing or order of execution.
# 1) Same payload at same time ( more than 1 user requests short code for same url at same time)
# one requests succeeds , other requests will cause integrity error as short code should be unique, but as the database does not have user specificness
#so return the same short code. 
# 2) Different payload with same hash codes which don't already exist, added the integrity error checks to handle that .


    
    





