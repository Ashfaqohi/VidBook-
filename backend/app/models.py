from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    id: str
    title: str
    topic: str
    description: str
    status: str
    created_at: str
    updated_at: str
