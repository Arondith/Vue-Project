import os

os.environ["DATABASE_URL"] = "sqlite://"

from fastapi.testclient import TestClient

from app.main import app


def sample_application() -> dict[str, object]:
    return {
        "company": "Acme Labs",
        "role": "Frontend Developer",
        "location": "Remote",
        "work_setup": "Remote",
        "status": "Applied",
        "salary": "$1,500/month",
        "job_url": "https://example.com/jobs/123",
        "notes": "Portfolio submitted",
        "applied_at": "2026-09-19",
    }


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_application_crud_and_stats() -> None:
    with TestClient(app) as client:
        created = client.post("/api/applications", json=sample_application())

        assert created.status_code == 201
        application_id = created.json()["id"]
        assert created.json()["company"] == "Acme Labs"

        listed = client.get("/api/applications")
        assert listed.status_code == 200
        assert len(listed.json()) == 1

        updated_payload = sample_application()
        updated_payload["status"] = "Interview"
        updated = client.put(
            f"/api/applications/{application_id}",
            json=updated_payload,
        )
        assert updated.status_code == 200
        assert updated.json()["status"] == "Interview"

        stats = client.get("/api/stats")
        assert stats.status_code == 200
        assert stats.json()["total"] == 1
        assert stats.json()["interview"] == 1

        deleted = client.delete(f"/api/applications/{application_id}")
        assert deleted.status_code == 204

        final_list = client.get("/api/applications")
        assert final_list.json() == []
