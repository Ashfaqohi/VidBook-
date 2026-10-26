import secrets
import sqlite3
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import get_db, init_db
from .schemas import (
    ApprovalCreate,
    ApprovalResponse,
    BookApprovalRequest,
    BookCreate,
    BookResponse,
    ClaimCreate,
    ClaimResponse,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    SourceCreate,
    SourceResponse,
)
from .storage import create_project_folders


def now() -> str:
    return datetime.now(UTC).isoformat()


def require_api_token(authorization: str | None = Header(default=None)) -> None:
    configured = get_settings().api_token
    if configured and not secrets.compare_digest(authorization or "", f"Bearer {configured}"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token")


def serialize_project(row: sqlite3.Row) -> ProjectResponse:
    return ProjectResponse(
        id=row["id"],
        title=row["title"],
        topic=row["topic"],
        description=row["description"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        folders=create_project_folders(row["id"]),
    )


def require_project(project_id: str, db: sqlite3.Connection) -> sqlite3.Row:
    row = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return row


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=get_settings().app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "vidbook-api"}


@app.get("/api/v1/projects", response_model=list[ProjectResponse], dependencies=[Depends(require_api_token)])
def list_projects(db: sqlite3.Connection = Depends(get_db)) -> list[ProjectResponse]:
    rows = db.execute("SELECT * FROM projects ORDER BY updated_at DESC").fetchall()
    return [serialize_project(row) for row in rows]


@app.post("/api/v1/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_token)])
def create_project(payload: ProjectCreate, db: sqlite3.Connection = Depends(get_db)) -> ProjectResponse:
    project_id = str(uuid4())
    timestamp = now()
    db.execute(
        "INSERT INTO projects (id, title, topic, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (project_id, payload.title.strip(), payload.topic.strip(), payload.description.strip(), timestamp, timestamp),
    )
    db.commit()
    row = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    return serialize_project(row)


@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse, dependencies=[Depends(require_api_token)])
def get_project(project_id: str, db: sqlite3.Connection = Depends(get_db)) -> ProjectResponse:
    row = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return serialize_project(row)


@app.patch("/api/v1/projects/{project_id}", response_model=ProjectResponse, dependencies=[Depends(require_api_token)])
def update_project(project_id: str, payload: ProjectUpdate, db: sqlite3.Connection = Depends(get_db)) -> ProjectResponse:
    existing = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="Project not found")
    changes = payload.model_dump(exclude_unset=True)
    if changes:
        assignments = ", ".join(f"{field} = ?" for field in changes)
        values = [value.strip() if isinstance(value, str) else value for value in changes.values()]
        db.execute(
            f"UPDATE projects SET {assignments}, updated_at = ? WHERE id = ?",
            (*values, now(), project_id),
        )
        db.commit()
    row = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    return serialize_project(row)


@app.delete("/api/v1/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_api_token)])
def delete_project(project_id: str, db: sqlite3.Connection = Depends(get_db)) -> None:
    result = db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    db.commit()


@app.post("/api/v1/projects/{project_id}/approvals/{stage}", response_model=ApprovalResponse, dependencies=[Depends(require_api_token)])
def record_approval(project_id: str, stage: str, payload: ApprovalCreate, db: sqlite3.Connection = Depends(get_db)) -> ApprovalResponse:
    project = db.execute("SELECT id FROM projects WHERE id = ?", (project_id,)).fetchone()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    timestamp = now()
    cursor = db.execute(
        "INSERT INTO approvals (project_id, stage, decision, note, created_at) VALUES (?, ?, ?, ?, ?)",
        (project_id, stage, payload.decision, payload.note.strip(), timestamp),
    )
    if payload.decision == "approve" and stage == "brief":
        db.execute("UPDATE projects SET status = 'brief_approved', updated_at = ? WHERE id = ?", (timestamp, project_id))
    db.commit()
    return ApprovalResponse(
        id=cursor.lastrowid,
        project_id=project_id,
        stage=stage,
        decision=payload.decision,
        note=payload.note.strip(),
        created_at=timestamp,
    )


@app.get("/api/v1/projects/{project_id}/books", response_model=list[BookResponse], dependencies=[Depends(require_api_token)])
def list_books(project_id: str, db: sqlite3.Connection = Depends(get_db)) -> list[BookResponse]:
    require_project(project_id, db)
    return [BookResponse(**dict(row)) for row in db.execute("SELECT * FROM books WHERE project_id = ? ORDER BY rank, credibility_score DESC", (project_id,)).fetchall()]


@app.post("/api/v1/projects/{project_id}/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_token)])
def create_book(project_id: str, payload: BookCreate, db: sqlite3.Connection = Depends(get_db)) -> BookResponse:
    require_project(project_id, db)
    book_id = str(uuid4())
    timestamp = now()
    db.execute(
        "INSERT INTO books (id, project_id, title, author, publication_year, publisher, relevance_score, credibility_score, accessibility, rationale, rank, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (book_id, project_id, payload.title.strip(), payload.author.strip(), payload.publication_year, payload.publisher.strip(), payload.relevance_score, payload.credibility_score, payload.accessibility.strip(), payload.rationale.strip(), payload.rank, timestamp),
    )
    db.commit()
    return BookResponse(**dict(db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()))


@app.post("/api/v1/projects/{project_id}/books/approve", response_model=list[BookResponse], dependencies=[Depends(require_api_token)])
def approve_books(project_id: str, payload: BookApprovalRequest, db: sqlite3.Connection = Depends(get_db)) -> list[BookResponse]:
    require_project(project_id, db)
    book_ids = list(dict.fromkeys(payload.book_ids))
    if len(book_ids) != 5:
        raise HTTPException(status_code=422, detail="Exactly five distinct books must be approved")
    placeholders = ",".join("?" for _ in book_ids)
    rows = db.execute(f"SELECT * FROM books WHERE project_id = ? AND id IN ({placeholders})", (project_id, *book_ids)).fetchall()
    if len(rows) != 5:
        raise HTTPException(status_code=400, detail="All approved books must belong to this project")
    timestamp = now()
    db.execute("UPDATE books SET approval_status = 'rejected' WHERE project_id = ?", (project_id,))
    db.execute(f"UPDATE books SET approval_status = 'approved' WHERE project_id = ? AND id IN ({placeholders})", (project_id, *book_ids))
    db.execute("UPDATE projects SET status = 'research', updated_at = ? WHERE id = ?", (timestamp, project_id))
    db.commit()
    approved = db.execute(f"SELECT * FROM books WHERE project_id = ? AND id IN ({placeholders}) ORDER BY rank", (project_id, *book_ids)).fetchall()
    return [BookResponse(**dict(row)) for row in approved]


@app.get("/api/v1/projects/{project_id}/sources", response_model=list[SourceResponse], dependencies=[Depends(require_api_token)])
def list_sources(project_id: str, db: sqlite3.Connection = Depends(get_db)) -> list[SourceResponse]:
    require_project(project_id, db)
    return [SourceResponse(**dict(row)) for row in db.execute("SELECT * FROM sources WHERE project_id = ? ORDER BY created_at DESC", (project_id,)).fetchall()]


@app.post("/api/v1/projects/{project_id}/sources", response_model=SourceResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_token)])
def create_source(project_id: str, payload: SourceCreate, db: sqlite3.Connection = Depends(get_db)) -> SourceResponse:
    require_project(project_id, db)
    source_id = str(uuid4())
    timestamp = now()
    db.execute(
        "INSERT INTO sources (id, project_id, kind, title, author, url, local_path, access_status, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (source_id, project_id, payload.kind.strip(), payload.title.strip(), payload.author.strip(), payload.url.strip(), payload.local_path.strip(), payload.access_status.strip(), payload.notes.strip(), timestamp),
    )
    db.commit()
    return SourceResponse(**dict(db.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()))


@app.get("/api/v1/projects/{project_id}/claims", response_model=list[ClaimResponse], dependencies=[Depends(require_api_token)])
def list_claims(project_id: str, db: sqlite3.Connection = Depends(get_db)) -> list[ClaimResponse]:
    require_project(project_id, db)
    return [ClaimResponse(**dict(row)) for row in db.execute("SELECT * FROM claims WHERE project_id = ? ORDER BY created_at DESC", (project_id,)).fetchall()]


@app.post("/api/v1/projects/{project_id}/claims", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_token)])
def create_claim(project_id: str, payload: ClaimCreate, db: sqlite3.Connection = Depends(get_db)) -> ClaimResponse:
    require_project(project_id, db)
    if payload.source_id:
        source = db.execute("SELECT id FROM sources WHERE id = ? AND project_id = ?", (payload.source_id, project_id)).fetchone()
        if source is None:
            raise HTTPException(status_code=400, detail="Source must belong to this project")
    claim_id = str(uuid4())
    timestamp = now()
    db.execute(
        "INSERT INTO claims (id, project_id, claim_text, claim_type, evidence_strength, verification_status, source_id, locator, supporting_passage, conflict_note, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (claim_id, project_id, payload.claim_text.strip(), payload.claim_type.strip(), payload.evidence_strength.strip(), payload.verification_status.strip(), payload.source_id, payload.locator.strip(), payload.supporting_passage.strip(), payload.conflict_note.strip(), timestamp, timestamp),
    )
    db.commit()
    return ClaimResponse(**dict(db.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()))
