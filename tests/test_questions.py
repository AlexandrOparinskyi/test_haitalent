import pytest
from fastapi import status

question_json = {
    "text": "checked text"
}


@pytest.mark.asyncio
async def test_get_empty_questions(client):
    res = await client.get("/questions/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_question(client):
    res = await client.post("/questions/", json=question_json)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["id"] == 1
    assert res.json()["text"] == question_json["text"]


@pytest.mark.asyncio
async def test_get_question_by_id(client):
    res = await client.get("/questions/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["id"] == 1
    assert res.json()["text"] == question_json["text"]


@pytest.mark.asyncio
async def test_get_questions(client):
    res = await client.get("/questions/")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 1


@pytest.mark.asyncio
async def test_delete_question(client):
    res = await client.delete("/questions/1")
    assert res.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_nonexisting_question(client):
    res = await client.get("/questions/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND
