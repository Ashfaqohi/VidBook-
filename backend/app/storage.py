from pathlib import Path

from .config import get_settings


PROJECT_FOLDERS = (
    "brief",
    "research",
    "sources",
    "evidence",
    "script",
    "production",
    "exports",
)


def create_project_folders(project_id: str) -> list[str]:
    project_root = get_settings().storage_path / project_id
    project_root.mkdir(parents=True, exist_ok=True)
    for folder in PROJECT_FOLDERS:
        (project_root / folder).mkdir(exist_ok=True)
    return list(PROJECT_FOLDERS)
