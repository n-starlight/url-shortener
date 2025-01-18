from fastapi import FastAPI,Header
from pydantic import BaseModel
from fastapi import HTTPException,Depends
import hashlib
from datetime import datetime
from typing import Union,AsyncGenerator
from sqlalchemy import select,delete,func,update
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import  AsyncSession
from db.conn_session import create_app
from db.schema import URL_SHORTENER,Users
from urllib.parse import urlparse
import socket
import string,random

load_dotenv()

app = create_app()

class LongUrl(BaseModel):
    url_link:str
    custom_slug:Union[str, None] = None

DOMAIN="https://heystarlette/"

#Scope of this will be to a specific route for a single specific request ,new session for each concurrent request when passed as dependency and using proper context scope.
async def get_session() -> AsyncGenerator[AsyncSession,None]:
    async_session=app.state.async_session
    async with async_session() as session:  # using with context manager opens the session on first execute and closes the async session (sesion) instance at the end of with block
        yield session


# Verbose explaination of how it will be used via dep.
# session_generator = get_session()
# session = await session_generator.__anext__()  async session instance 
# Use the session for database operations

 
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

async def save_url(session,userid,original_url:str,short_code:str):
    new_url=URL_SHORTENER(original_url=original_url,short_code=short_code,user_id=userid)
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
           select(URL_SHORTENER).where(URL_SHORTENER.short_code==short_code)
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

def is_valid_url(url: str):
    """
    Validate the URL format and check if it's secure and resolved to a valid domain.
    """
    parsed = urlparse(url)
    # "scheme://netloc/path;parameters?query#fragment"

    try:
        # Check for valid scheme and netloc
        if parsed.scheme not in ["http", "https"] or not bool(parsed.netloc):
            return False
        hostname = parsed.netloc.split(":")[0]

        #check if hostname resolves to an ip address (i.e. domain exists)
        hostip=socket.gethostbyname(hostname)

        return hostip and True
    
    except (ValueError,socket.gaierror) :
        return False
    
def random_code(min_length=5,max_length=8):
    #Hash the url with the time entropy for randomness for same url 
    chars=string.ascii_letters + string.digits
    return "".join(random.choices(chars,k=2))


def hash_code_with_entropy(url,min_length=5,max_length=8):
    #Hash the url with the time entropy for randomness for same url 
    full_hash_rand=hashlib.sha256(f"{url}{datetime.now()}".encode()).hexdigest()
    length=random.randint(min_length,max_length)
    short_hash=full_hash_rand[:length+1]
    return short_hash


async def retry_ifnot_unq(short_code:str,url,session):
    
    max_attempts = 5
    attempts = 0
    while True:
        hash_code_new = hash_code_with_entropy(url)+random_code()
        code_exists=await check_code_exists(session,hash_code_new) 
        code_exists_scode=code_exists.URL_SHORTENER.short_code if code_exists else None 
        if not code_exists_scode:
            break
        attempts+=1

        if attempts>=max_attempts:
            raise HTTPException(status_code=500,detail='couldn''t generate unique code')
        
    short_code=hash_code_new
    return short_code
    
async def get_id_of_api_key(api_key,session):
    stmt=select(Users.id).where(Users.api_key==api_key)
    result=await session.execute(stmt)
    return result.first()
    

@app.post("/shorten")
async def shorten_url(payload:LongUrl,api_key:str=Header(...),db_session:AsyncSession=Depends(get_session)): 
    if not is_valid_url(payload.url_link):
        raise HTTPException(
            status_code=400, detail="Invalid or insecure URL format.")
    
    get_user_id_reqst=await get_id_of_api_key(api_key,db_session)
    if not get_user_id_reqst:
        raise HTTPException(status_code=403,detail="Not a valid api key")
    
    user_id_reqst=get_user_id_reqst.id

    hash_code=hash_code_with_entropy(payload.url_link)
    code_exists=await check_code_exists(db_session,hash_code)
    code_exists_scode=code_exists.short_code if code_exists else None

    
    if code_exists_scode:
        short_code=await retry_ifnot_unq(hash_code,payload.url_link,db_session)
        newinsert= await save_url(db_session,user_id_reqst,original_url=payload.url_link,short_code=short_code)
        print('newinsert',newinsert)
        response={"short_url":f"{newinsert.short_code}"}
            
    else:
        short_code=hash_code
        newinsert=await save_url(db_session,user_id_reqst,original_url=payload.url_link,short_code=short_code)
        print('newinsert',newinsert)
        response={"short_url":f"{newinsert.short_code}"}
    
    return response




@app.get("/redirect")
async def redirect_url(short_code:str,db_session:AsyncSession=Depends(get_session)):
    stmt=(
        update(URL_SHORTENER)
        .where(URL_SHORTENER.short_code == short_code)
        .values(
            last_accessed_at=datetime.now(),
            visit_cnt=(URL_SHORTENER.visit_cnt + 1)
        )
        .returning(URL_SHORTENER.original_url,URL_SHORTENER.visit_cnt)
    )

    result=await db_session.execute(stmt)
    url=result.first() if result else None
    # print("vist_cnt",url.visit_cnt)

    if url is None:
       raise HTTPException(status_code=404, detail="URL not found")
    
    await db_session.commit()
    print("url",url)
    return RedirectResponse(url=url.original_url,status_code=307)
    # response = {"original_url": url}
    # return response


async def del_scode(session,short_code):
    await session.execute(delete(URL_SHORTENER).where(URL_SHORTENER.short_code==short_code))
    await session.commit()

async def user_owns_code(apikey,scode,session):
    stmt1=select(URL_SHORTENER.user_id).where(URL_SHORTENER.short_code==scode)
    stmt2=select(Users.id).where(Users.api_key==apikey)

    result1=await session.execute(stmt1)
    result1=result1.first() if result1 else None
    result2=await session.execute(stmt2) 
    result2=result2.first() if result2 else None

    return (result1,result2)

    
@app.delete("/shorten/{short_code}")
async def remove_scode(short_code:str,api_key:str=Header(...),db_session:AsyncSession=Depends(get_session)):
    result1,result2=await user_owns_code(api_key,short_code,db_session) 
    
    if result1 :
        if result2 :
            if result1.user_id==result2.id:
                await del_scode(db_session,short_code)
                return {"message": f"{short_code} short code has been deleted"}
            return False
        else:
            raise HTTPException(status_code=403,detail="Not a valid api key")
    else:
        raise HTTPException(status_code=404,detail='Not a valid short code')
    

async def get_real_time_analytics(session,limit,offset):
    result=await session.execute(
           select(URL_SHORTENER).order_by(URL_SHORTENER.created_at.desc()).limit(limit)
        )
    # statement2=select(func.count(URL_SHORTENER.short_code).label("total_urls"))
    # result2=await session.execute(statement2)
    # print(result2.fetchone()) #(10001057,)
    scalars=result.scalars()
    result=scalars.all()
    print("scalars result" , scalars) # <sqlalchemy.engine.result.ScalarResult object at 0x000001CDAE829680>
    print("result all",result) #[<db.schema.URL_SHORTENER object at 0x000001CDAEE30C10>, <db.schema.URL_SHORTENER object at 0x000001CDAEA072D0>, ...
    return result

# query parameters can be passed if expected to return more than 10 latest urls, also query parameters are optional to specify
@app.get("/analytics/real-time")
async def real_time_analytics(db_session:AsyncSession=Depends(get_session), limit:int=10, offset:int=0):
    data = await get_real_time_analytics(db_session,limit,offset)
    if not data:
        raise HTTPException(status_code=404, detail="Error in getting real time analytics")
    # return [row.to_dict() for row in data]
    return data

# Handling of race conditions --
#A race condition occurs when two or more processes or threads attempt to perform an operation on shared resources simultaneously in such a way 
# that the outcome depends on the timing or order of execution.
# 1) Same payload at same time ( more than 1 user requests short code for same url at same time)
# one requests succeeds , other requests will cause integrity error as short code should be unique, but as the database does not have user specificness
#so return the same short code. 
# 2) Different payload with same hash codes which don't already exist, added the integrity error checks to handle that .


    
    





