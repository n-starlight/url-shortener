from fastapi.security import HTTPBearer, http
from fastapi import Request,status,HTTPException
from .utils import decode_token
from abc import ABC,abstractmethod

class TokenBearer(ABC,HTTPBearer):
    def __init__(self,auto_error=True):
        HTTPBearer.__init__(self,auto_error=auto_error)
    
    async def __call__(self,request:Request)->http.HTTPAuthorizationCredentials|None:
        authCreds=await HTTPBearer.__call__(self,request)
        token=authCreds.credentials
        
        decodedT=decode_token(token)
        
        if not decodedT:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid or expired token")
        
        self.tokenType(decodedT)
        return decodedT
        
        
    @abstractmethod
    def tokenType(self,decodedToken):
        pass

    
class AccessTokenBearer(TokenBearer):
    def tokenType(self,decodedT:dict):
        if decodedT and decodedT["refresh"]:
            raise HTTPException(status_code=400,detail="Please provide valid access token")
 
    
class RefreshTokenBearer(TokenBearer):
    def tokenType(self,decodedT:dict):
        if decodedT and not decodedT["refresh"]:
            raise HTTPException(status_code=400,detail="Please provide valid refresh token")
      




