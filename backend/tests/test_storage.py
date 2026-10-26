from pathlib import Path
from types import SimpleNamespace

from app import storage
from app.config import Settings


def test_create_project_folders_builds_the_expected_layout(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(storage, "get_settings", lambda: SimpleNamespace(storage_path=tmp_path))

    folders = storage.create_project_folders("project-1")

    assert folders == list(storage.PROJECT_FOLDERS)
    assert all((tmp_path / "project-1" / folder).is_dir() for folder in folders)


def test_settings_parse_multiple_cors_origins():
    settings = Settings(cors_origins="http://localhost:5173, https://studio.example")

    assert settings.cors_origin_list == ["http://localhost:5173", "https://studio.example"]
