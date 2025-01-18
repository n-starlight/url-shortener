
# from .main_no_orm import app
# from .main import app
from .main_new import app
import pytest
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine





@pytest.mark.anyio
async def test_post():
    async with LifespanManager(app):
         input_url="https://docs.sqlalchemy.org/en/20/core/constraints.html"
         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            post_response=await ac.post('/shorten',json={"url_link":input_url,"custome_slug":None},headers={"api-key":"hCxN5ak5h-5CkDN6bEz72WpM5n43MHioVlfcx_sa80E"})
            assert post_response.status_code == 200 
            post_res=post_response.json()
            assert post_res is not None

            response_invalid_userkey=await ac.post('/shorten',json={"url_link":input_url,"custome_slug":None},headers={"api-key":"hCxN5ak5h-5CkDN6bEz"})
            assert response_invalid_userkey.status_code == 403
            assert response_invalid_userkey.json()=={"detail":"Not a valid api key"}
    

          
@pytest.mark.anyio      
async def test_get():  
       async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            short_code="1e1052"
            input_url="https://grafana.com/docs/k6/latest/extensions/"
            get_response=await ac.get(f'/redirect?short_code={short_code}',follow_redirects=False)
            assert get_response.status_code == 307
            get_res=get_response.headers["Location"]
            assert get_res==input_url
            
            incorrect_scode="codedoesnotexist"
            get_response2=await ac.get(f'/redirect?short_code={incorrect_scode}',follow_redirects=False)
            assert get_response2.status_code == 404
            assert get_response2.json()== {"detail":"URL not found"}

@pytest.mark.anyio      
async def test_del():
       async with LifespanManager(app):  
           async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
              
              response_invalid_key = await ac.delete(f"/shorten/cd6f68a",headers={"api-key":"yyyy"})
              assert response_invalid_key.status_code == 403
              assert response_invalid_key.json()=={"detail":"Not a valid api key"}
              

              incorrect_scode="incorrect_code"
              response_invalid_scode = await ac.delete(f"/shorten/{incorrect_scode}",headers={"api-key":"EcRGiU5nK8e90-eBMT2k-abcoEsZPYw9bTmcw_V6O8w"})
              assert response_invalid_scode.status_code == 404
              assert response_invalid_scode.json()=={"detail":"Not a valid short code"}
              
              del_response=await ac.delete(f'/shorten/68a4d434',headers={"api-key":"EcRGiU5nK8e90-eBMT2k-abcoEsZPYw9bTmcw_V6O8w"})
              assert del_response.status_code==200
              assert del_response.json()== {"message": f"68a4d434 short code has been deleted"}
