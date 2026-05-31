from __future__ import annotations

from app import app, list_draft_files, list_modules


def test_list_draft_files_includes_starbucks_notebooks() -> None:
    draft_files = list_draft_files()

    assert "StarbucksNotebook1.txt" in draft_files


def test_list_modules_includes_narrative_synopsis() -> None:
    modules = list_modules()

    assert "001-Narrative_Synopsis" in modules


def test_home_route_loads() -> None:
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Prompt Control Panel" in response.data


def test_home_post_compiles_prompt() -> None:
    client = app.test_client()

    response = client.post(
        "/",
        data={
            "draft_file": "StarbucksNotebook1.txt",
            "module": "001-Narrative_Synopsis",
        },
    )

    assert response.status_code == 200
    assert b"Prompt compiled successfully." in response.data
    assert b"001-Narrative_Synopsis Prompt" in response.data
