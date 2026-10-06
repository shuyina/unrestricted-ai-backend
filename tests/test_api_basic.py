import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_api_v1_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_image_generation_schema():
    payload = {
        "prompt": "A beautiful landscape",
        "negative_prompt": "",
        "width": 1024,
        "height": 1024,
        "steps": 30,
        "guidance_scale": 7.5,
    }
    response = client.post("/api/v1/generate/image/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert data["mode"] == "text_to_image"
    assert "job_id" in data


def test_video_generation_schema():
    payload = {
        "prompt": "A spinning cube",
        "duration_seconds": 5,
        "fps": 24,
    }
    response = client.post("/api/v1/generate/video/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert data["mode"] == "text_to_video"


def test_faceswap_schema():
    payload = {
        "source_image_url": "https://example.com/source.jpg",
        "target_image_url": "https://example.com/target.jpg",
        "method": "roop",
    }
    response = client.post("/api/v1/faceswap/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert data["mode"] == "face_swap"


def test_llm_chat_schema():
    payload = {
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "model": "llama3",
    }
    response = client.post("/api/v1/llm/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert "response" in data
