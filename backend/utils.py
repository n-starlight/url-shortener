from passlib.context import CryptContext
import secrets,os,jwt,uuid,logging
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime ,timedelta

load_dotenv()

pass_context=CryptContext(schemes=['bcrypt'])

SECRET_KEY=os.getenv("SUPER_SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7



class TokenData(BaseModel):
    email:str

def gen_password_hash(password:str):
    hashp=pass_context.hash(password)
    return hashp

def verify_pass(passowrd:str,hash:str):
    return pass_context.verify(passowrd,hash)

def generate_api_key():
    return secrets.token_urlsafe(32)  # Generates a 43-character base64 string(A-Z,a-z,0-9)

def create_token(userIdentity:dict,expires_time:timedelta=None,refresh:bool=False):
    to_encode={}
    to_encode["userIdty"]=userIdentity
    if refresh:
        expiry=datetime.now() + (expires_time or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    else:
        expiry=datetime.now() + (expires_time if expires_time is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"]=expiry
    to_encode["jti"]=str(uuid.uuid4())
    to_encode["refresh"]=refresh
    token= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

# def create_refresh_token(userEmail:str):
#     expiry=datetime.now() + (timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
#     to_encode={"identity":userEmail,"expiry":expiry}
#     return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def decode_token(token:str):
    try:
        token_data=jwt.decode(
        jwt=token,
        key=SECRET_KEY,
        algorithms=ALGORITHM
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None