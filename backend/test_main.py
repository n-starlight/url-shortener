from fastapi.testclient import TestClient 
from fastapi.responses import RedirectResponse
from .main import app

client=TestClient(app)

API_URL="http://127.0.0.1:8000/"

def test_endpoints():
    input_url="https://example.com"
    post_response=client.post('/shorten',json={"url_link":input_url,"custome_slug":None})
    assert post_response.status_code == 200 
    post_res=post_response.json()
    short_url=post_res["short_url"]
    short_code=short_url

    get_response=client.get(f'/redirect?short_code={short_code}')
    assert get_response.status_code == 200
    get_res=get_response.json()["original_url"]
    assert get_res==input_url

    
    response2=client.post('/shorten',json={"url_link":input_url,"custome_slug":None})
    assert response2.status_code == 200
    res2_short_code=response2.json()["short_url"]
    assert short_code == res2_short_code
    