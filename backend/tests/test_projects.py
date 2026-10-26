from pathlib import Path

from fastapi.testclient import TestClient


def test_project_crud_and_approval(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("VIDBOOK_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("VIDBOOK_STORAGE_PATH", str(tmp_path / "projects"))

    from app.config import get_settings
    from app.main import app

    get_settings.cache_clear()
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/projects",
            json={"title": "Silk Roads", "topic": "Trade across Eurasia", "description": "A focused pilot."},
        )
        assert created.status_code == 201
        project = created.json()
        assert project["status"] == "brief_pending"
        assert (tmp_path / "projects" / project["id"] / "research").is_dir()

        listing = client.get("/api/v1/projects")
        assert listing.status_code == 200
        assert listing.json()[0]["id"] == project["id"]

        approval = client.post(
            f"/api/v1/projects/{project['id']}/approvals/brief",
            json={"decision": "approve", "note": "Scope is clear."},
        )
        assert approval.status_code == 200
        assert client.get(f"/api/v1/projects/{project['id']}").json()["status"] == "brief_approved"


def test_missing_project_returns_404(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("VIDBOOK_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("VIDBOOK_STORAGE_PATH", str(tmp_path / "projects"))

    from app.config import get_settings
    from app.main import app

    get_settings.cache_clear()
    with TestClient(app) as client:
        assert client.get("/api/v1/projects/not-found").status_code == 404


def test_book_shortlist_requires_and_approves_exactly_five(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("VIDBOOK_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("VIDBOOK_STORAGE_PATH", str(tmp_path / "projects"))

    from app.config import get_settings
    from app.main import app

    get_settings.cache_clear()
    with TestClient(app) as client:
        project = client.post("/api/v1/projects", json={"title": "A History", "topic": "A focused question"}).json()
        book_ids = []
        for number in range(6):
            response = client.post(
                f"/api/v1/projects/{project['id']}/books",
                json={"title": f"Book {number}", "author": "Author", "rank": number + 1, "credibility_score": 80},
            )
            assert response.status_code == 201
            book_ids.append(response.json()["id"])

        assert client.post(f"/api/v1/projects/{project['id']}/books/approve", json={"book_ids": book_ids[:4]}).status_code == 422
        approved = client.post(f"/api/v1/projects/{project['id']}/books/approve", json={"book_ids": book_ids[:5]})
        assert approved.status_code == 200
        assert len(approved.json()) == 5
        assert client.get(f"/api/v1/projects/{project['id']}").json()["status"] == "research"
        assert client.get(f"/api/v1/projects/{project['id']}/books").json()[-1]["approval_status"] == "rejected"


def test_sources_and_claims_are_project_scoped(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("VIDBOOK_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("VIDBOOK_STORAGE_PATH", str(tmp_path / "projects"))

    from app.config import get_settings
    from app.main import app

    get_settings.cache_clear()
    with TestClient(app) as client:
        project = client.post("/api/v1/projects", json={"title": "Evidence", "topic": "A claim"}).json()
        source = client.post(f"/api/v1/projects/{project['id']}/sources", json={"kind": "archive", "title": "Archive record", "access_status": "accessible"})
        assert source.status_code == 201
        claim = client.post(f"/api/v1/projects/{project['id']}/claims", json={"claim_text": "A documented event occurred.", "claim_type": "fact", "source_id": source.json()["id"], "locator": "p. 12", "verification_status": "verified"})
        assert claim.status_code == 201
        assert client.get(f"/api/v1/projects/{project['id']}/claims").json()[0]["source_id"] == source.json()["id"]
