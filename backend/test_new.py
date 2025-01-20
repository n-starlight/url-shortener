
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

            post_response=await ac.post('/shorten',json={"url_link":input_url,"custom_slug":None,"exp_date":None},headers={"api-key":"hCxN5ak5h-5CkDN6bEz72WpM5n43MHioVlfcx_sa80E"})
            assert post_response.status_code == 200 
            assert post_response.json() is not None

            response_invalid_userkey=await ac.post('/shorten',json={"url_link":input_url,"custom_slug":None,"exp_date":None},headers={"api-key":"hCxN5ak5h-5CkDN6bEz"})
            assert response_invalid_userkey.json()["error_code"] == 403
            assert response_invalid_userkey.json()["error_detail"]=="Not a valid api key"

            response_invalid_url=await ac.post('/shorten',json={"url_link":"","custom_slug":None,"exp_date":None},headers={"api-key":"hCxN5ak5h-5CkDN6bEz72WpM5n43MHioVlfcx_sa80E"})
            assert response_invalid_url.json()["error_code"] == 400
            assert response_invalid_url.json()["error_detail"]=="Invalid or insecure URL format"

            correct_form_exp=await ac.post('/shorten',json={"url_link":input_url,"exp_date":"2025-02-01"},headers={"api-key":"hCxN5ak5h-5CkDN6bEz72WpM5n43MHioVlfcx_sa80E"})
            assert correct_form_exp.status_code == 200 
            assert correct_form_exp.json() is not None

            # custome_slug_unq=await ac.post('/shorten',json={"url_link":input_url,"custom_slug":"sqlcotre"},headers={"api-key":"NtI8xTE2_M9T8AistPV4I165QwwpN4th4SdEtfbITFs"})
            # assert custome_slug_unq.status_code == 200 
            # assert custome_slug_unq.json() is not None

            custome_slug_nonunq=await ac.post('/shorten',json={"url_link":input_url,"custom_slug":"sqalconsre"},headers={"api-key":"NtI8xTE2_M9T8AistPV4I165QwwpN4th4SdEtfbITFs"})
            assert custome_slug_nonunq.json()["error_code"]== 409 
            assert custome_slug_nonunq.json()["error_detail"] =="Code already exits, Retry"

            body_as_list=await ac.post('/shorten',json=[{"url_link":input_url,"custom_slug":None,"exp_date":None},{"url_link":input_url,"custom_slug":"sqalconsre","exp_date":None}],
                          headers={"api-key":"hCxN5ak5h-5CkDN6bEz72WpM5n43MHioVlfcx_sa80E"})
            assert body_as_list.status_code == 200 
            assert body_as_list.json()["successes"] is not None
            assert body_as_list.json()["failures"] is not None
    

          
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

            expired_code="e8b00d2e6"
            expired_code_res=await ac.get(f'/redirect?short_code={expired_code}',follow_redirects=False)
            assert expired_code_res.status_code==410
            assert expired_code_res.json()=={"detail":"Code already expired"}


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
