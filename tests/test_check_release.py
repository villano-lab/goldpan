"""Tests for tools/check_release.py: the tag of a goldpan release must agree with the code before it is published."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_release as cr  # noqa: E402

CHANGELOG = """# Changelog

## [Unreleased]

- something new

## [0.3.0] - 2026-11-04

- the last release made in NSDF-Data.
"""


def tree(tmp_path, pyproject="0.3.0", changelog=CHANGELOG):
    (tmp_path / "pyproject.toml").write_text(f'[project]\nname = "goldpan"\nversion = "{pyproject}"\n', encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
    return tmp_path


def test_version_of_accepts_only_vXYZ_tags():
    assert cr.version_of("v0.3.0") == "0.3.0" and cr.version_of("v10.20.30") == "10.20.30"
    for bad in ("0.3.0", "goldpan-v0.3.0", "v0.3", "v0.3.0rc1", "xv0.3.0", ""):
        assert cr.version_of(bad) is None, bad


def test_a_consistent_release_has_no_problems(tmp_path):
    assert cr.problems("v0.3.0", tree(tmp_path)) == []


def test_other_tags_are_refused(tmp_path):
    (msg,) = cr.problems("goldpan-v0.3.0", tree(tmp_path))
    assert "vX.Y.Z" in msg


def test_the_version_must_agree_with_the_tag(tmp_path):
    (msg,) = cr.problems("v0.3.0", tree(tmp_path, pyproject="0.2.9"))
    assert "0.2.9" in msg and "0.3.0" in msg


def test_the_changelog_needs_a_released_section(tmp_path):
    assert cr.problems("v0.4.0", tree(tmp_path, pyproject="0.4.0"))                     # only [Unreleased] and [0.3.0]
    assert cr.problems("v0.3.0", tree(tmp_path, changelog="## [Unreleased]\n\n- x\n"))
    assert cr.problems("v0.3.0", tree(tmp_path, changelog="## [0.30.0] - 2026-11-05\n"))   # another version


def test_main_returns_the_exit_code(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(cr, "ROOT", tree(tmp_path))
    assert cr.main(["x", "v0.3.0"]) == 0 and "ready to publish goldpan 0.3.0" in capsys.readouterr().out
    assert cr.main(["x", "v0.5.0"]) == 1 and "ERROR" in capsys.readouterr().out
    assert cr.main(["x", "--version-only", "v0.3.0"]) == 0 and capsys.readouterr().out.strip() == "0.3.0"
    assert cr.main(["x"]) == 2


def test_the_real_repository_has_a_released_section_for_its_version():
    version = cr.tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    assert cr.problems(f"v{version}") == []


def test_the_workflow_publishes_only_from_tags_with_a_trusted_publisher():
    text = (ROOT / ".github" / "workflows" / "publish-goldpan.yml").read_text(encoding="utf-8")
    assert 'tags: ["v*"]' in text and "id-token: write" in text and "environment:" in text
    assert "if: github.ref_type == 'tag'" in text and "pypa/gh-action-pypi-publish" in text
    for forbidden in ("password:", "PYPI_TOKEN", "secrets."):
        assert forbidden not in text, f"the workflow must not use {forbidden}: PyPI trusts the workflow, no token is stored"
