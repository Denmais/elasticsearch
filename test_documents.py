import os
import pytest
from httpx import AsyncClient
import uuid

@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def api_context():

    async with AsyncClient(
        base_url=os.getenv("APP_URL", "http://127.0.0.1:8000"),
        timeout=10.0,
        trust_env=False,
    ) as client:
        yield client


@pytest.mark.anyio
async def test_create_get_search(api_context: tuple[AsyncClient, list[str]]):
    client = api_context
    id = uuid.uuid4()
    payload = {"text": f"Привет новый мир, это тестовый бот {id}", 
               "rubrics": ["VK-test"], 
               "created_date": "2019-05-16T05:59:36Z"
               }

    created = await client.post("/documents", json=payload)
    assert created.status_code == 200, created.text

    doc = created.json()
    doc_id = doc["id"]
    print(doc)

    assert doc["text"] == payload["text"]
    assert doc["rubrics"] == ["VK-test"]
    assert doc["created_date"] == "2019-05-16T05:59:36Z"

    ls = await client.get("/documents", params={"limit": 100})
    assert ls.status_code == 200, ls.text
    assert doc in ls.json()

    f = await client.get("/documents/search", params={"q": f"{id}"})
    assert f.status_code == 200, f.text
    print(f)
    assert f.json() == [doc]

    removed = await client.delete(f"/documents/{doc_id}")
    assert removed.status_code == 204, removed.text
    assert removed.content == b""

    ls_a= await client.get("/documents", params={"limit": 100})
    f_a = await client.get("/documents/search", params={"q": f"{id}"})

    assert ls_a.status_code == 200, ls_a.text
    assert all(item["id"] != doc_id for item in ls_a.json())
    assert f_a.status_code == 200, f_a.text
    assert f_a.json() == []
