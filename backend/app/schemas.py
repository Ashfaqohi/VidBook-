from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


ProjectStatus = Literal[
    "brief_pending",
    "brief_approved",
    "research",
    "evidence_review",
    "thesis_review",
    "script_review",
    "production",
    "qa",
    "complete",
]


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    topic: str = Field(min_length=1, max_length=500)
    description: str = Field(default="", max_length=4000)


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=160)
    topic: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=4000)
    status: ProjectStatus | None = None


class ProjectResponse(BaseModel):
    id: str
    title: str
    topic: str
    description: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    folders: list[str]


class ApprovalCreate(BaseModel):
    decision: Literal["approve", "reject", "changes_requested"]
    note: str = Field(default="", max_length=4000)


class ApprovalResponse(BaseModel):
    id: int
    project_id: str
    stage: str
    decision: str
    note: str
    created_at: datetime


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    author: str = Field(min_length=1, max_length=200)
    publication_year: int | None = Field(default=None, ge=1000, le=2100)
    publisher: str = Field(default="", max_length=200)
    relevance_score: float = Field(default=0, ge=0, le=100)
    credibility_score: float = Field(default=0, ge=0, le=100)
    accessibility: str = Field(default="unknown", max_length=80)
    rationale: str = Field(default="", max_length=4000)
    rank: int = Field(default=0, ge=0)


class BookResponse(BookCreate):
    id: str
    project_id: str
    approval_status: str
    created_at: datetime


class BookApprovalRequest(BaseModel):
    book_ids: list[str] = Field(min_length=5, max_length=5)


class SourceCreate(BaseModel):
    kind: str = Field(min_length=1, max_length=80)
    title: str = Field(min_length=1, max_length=300)
    author: str = Field(default="", max_length=200)
    url: str = Field(default="", max_length=2000)
    local_path: str = Field(default="", max_length=1000)
    access_status: str = Field(default="unverified", max_length=80)
    notes: str = Field(default="", max_length=4000)


class SourceResponse(SourceCreate):
    id: str
    project_id: str
    created_at: datetime


class ClaimCreate(BaseModel):
    claim_text: str = Field(min_length=1, max_length=4000)
    claim_type: str = Field(min_length=1, max_length=80)
    evidence_strength: str = Field(default="unassessed", max_length=80)
    verification_status: str = Field(default="unverified", max_length=80)
    source_id: str | None = None
    locator: str = Field(default="", max_length=500)
    supporting_passage: str = Field(default="", max_length=8000)
    conflict_note: str = Field(default="", max_length=4000)


class ClaimResponse(ClaimCreate):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
