from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException,Depends
import hashlib
from typing import Union
from sqlalchemy import text
from fastapi.responses import RedirectResponse

from db.connection import get_db_connection

app = FastAPI()



class LongUrl(BaseModel):
    url_link:str
    custom_slug:Union[str, None] = None


@app.get("/")
def read_root():
    return {"Url shortener active"}

def check_code_exists(conn,short_code:str):
    query=text("""SELECT 1 FROM url_shortener WHERE short_code = :short_code """) #short_code is indexed
    result=conn.execute(query,{"short_code":short_code}) # will result to None for empty result
    print(f'result.fetchone(){result.fetchone()},result :{result}')
    return result.fetchone() != None

def retry_ifnot_unq(short_code:str,payload,db_conn):
    
    max_attempts = 5
    attempts = 0
    while True:
        
        if not check_code_exists(db_conn,short_code):
            break
        attempts+=1

        if attempts>=max_attempts:
            raise HTTPException(status_code=500,detail='Please enter a unique code ,couldn''t generate unique code')
    
        short_code = hashlib.md5(f"{payload.url_link}{attempts}".encode()).hexdigest()[:6]
    return short_code

def save_url(conn,original_url:str,short_code:str):
    query=text("""
        INSERT INTO url_shortener(original_url, short_code)
        VALUES(:original_url,:short_code)
        RETURNING id, original_url, short_code, created_at;   
    """)  # as we are not projecting the result so returning,like it will still create it(result) but result.fetchone() won't work 
    #and error will be shown in response body
    result=conn.execute(query,{"original_url": original_url, "short_code": short_code})
    conn.commit() # necessary to commit explicitly as when post called again (new transaction) it won't be able to see changes
    print("result",result)
    fetchresult=result.fetchone()
    print("resultfetch",fetchresult)
    return fetchresult

def get_url(short_code,conn):
    query=text(""" SELECT original_url FROM url_shortener WHERE short_code = :short_code """)
    result=conn.execute(query,{"short_code":short_code})
    fetchresult=result.fetchone()
    print("res",fetchresult)
    return fetchresult[0] if fetchresult else None


@app.post("/shorten")
def shorten_url(payload:LongUrl,db_conn=Depends(get_db_connection)):  
    if short_code:
        if check_code_exists(db_conn,short_code):
            raise HTTPException(status_code=500,detail='Please enter a unique code ,it already exists')
    
    else:
        hash_code=hashlib.md5(payload.url_link.encode()).hexdigest()[:6]
        short_code=retry_ifnot_unq(hash_code,payload,db_conn)

    newinsert= save_url(db_conn,original_url=payload.url_link,short_code=short_code)
    print('newinsert',newinsert)
    # print(newinsert[2])
    # print(newinsert[0])
    response={"short_url":f"https://heystarlette/{newinsert[2]}"}

    return response


@app.get("/redirect")
def redirect_url(short_code:str,db_conn=Depends(get_db_connection)):
    url=  get_url(short_code,db_conn)
    if not url:
       raise HTTPException(status_code=404, detail="URL not found")
    print("url",url)
    return RedirectResponse(url=url)
    # response = {"original_url": url}
    # return response


# change to  async mode when needed later 
    
    




