
# from .main_no_orm import app
# # from .main import app
# import pytest
# from httpx import ASGITransport, AsyncClient
# # from asgi_lifespan import LifespanManager


# API_URL="http://127.0.0.1:8000/"
# input_url="https://example.com"

# @pytest.mark.anyio
# async def test_endpoints():
#     # async with LifespanManager(app):
#          async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#             post_response=await ac.post('/shorten',json={"url_link":input_url,"custome_slug":None})
#             assert post_response.status_code == 200 
#             post_res=post_response.json()
#             assert post_res is not None
#             print(post_res)
#             short_url=post_res["short_url"]
#             print("short url",short_url)
#             short_code=short_url
    
       
#             response2=await ac.post('/shorten',json={"url_link":input_url,"custome_slug":None})
#             assert response2.status_code == 200
#             res2_short_code=response2.json()["short_url"]
#             assert res2_short_code is not None
#             assert short_code == res2_short_code

#         #    short_code="1e1052"
#         #    input_url="https://grafana.com/docs/k6/latest/extensions/"
#             get_response=await ac.get(f'/redirect?short_code={short_code}',follow_redirects=False)
#             assert get_response.status_code == 307
#             get_res=get_response.headers["Location"]
#             assert get_res==input_url
        
      
      

   
    