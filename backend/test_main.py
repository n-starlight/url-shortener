from fastapi.testclient import TestClient

from .main import app

client=TestClient(app)

def test_endpoints():
    input_url="https://example.com"
    post_response=client.post('/shorten',json={"url_link":input_url,"custome_slug":None})
    assert post_response.status_code == 200 
    post_res=post_response.json()
    short_url=post_res["short_url"]
    short_code=short_url.split("/")[-1]

    get_response=client.get(f'/redirect?short_code={short_code}')
    assert get_response.status_code == 200
    get_res=get_response.json()
    assert get_res["original_url"] == input_url
    