import sqlite3
from collections.abc import Generator
from pathlib import Path

from .config import get_settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'brief_pending',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    stage TEXT NOT NULL,
    decision TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_projects_updated_at ON projects(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_approvals_project_id ON approvals(project_id);

CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_year INTEGER,
    publisher TEXT NOT NULL DEFAULT '',
    relevance_score REAL NOT NULL DEFAULT 0,
    credibility_score REAL NOT NULL DEFAULT 0,
    accessibility TEXT NOT NULL DEFAULT 'unknown',
    rationale TEXT NOT NULL DEFAULT '',
    rank INTEGER NOT NULL DEFAULT 0,
    approval_status TEXT NOT NULL DEFAULT 'candidate',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL DEFAULT '',
    url TEXT NOT NULL DEFAULT '',
    local_path TEXT NOT NULL DEFAULT '',
    access_status TEXT NOT NULL DEFAULT 'unverified',
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claims (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    claim_text TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    evidence_strength TEXT NOT NULL DEFAULT 'unassessed',
    verification_status TEXT NOT NULL DEFAULT 'unverified',
    source_id TEXT REFERENCES sources(id) ON DELETE SET NULL,
    locator TEXT NOT NULL DEFAULT '',
    supporting_passage TEXT NOT NULL DEFAULT '',
    conflict_note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_books_project_id ON books(project_id);
CREATE INDEX IF NOT EXISTS idx_sources_project_id ON sources(project_id);
CREATE INDEX IF NOT EXISTS idx_claims_project_id ON claims(project_id);
"""


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with _connect(get_settings().db_path) as connection:
        connection.executescript(SCHEMA)


def get_db() -> Generator[sqlite3.Connection, None, None]:
    connection = _connect(get_settings().db_path)
    try:
        yield connection
    finally:
        connection.close()
