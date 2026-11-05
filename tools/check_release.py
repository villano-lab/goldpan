"""Check the tag of a goldpan release before it is published to PyPI (used by .github/workflows/publish-goldpan.yml).

    python tools/check_release.py v0.4.0

Before anything is uploaded the tag must agree with the code:

* it has the form `vX.Y.Z`;
* `version` in `pyproject.toml` says `X.Y.Z`;
* CHANGELOG.md has a released section `## [X.Y.Z]` (not only `[Unreleased]`).

Prints the problems and exits 1 if there are any; prints the version and exits 0 if not. `--version-only TAG` prints just the
version of a well-formed tag.
"""
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = re.compile(r"^v(\d+\.\d+\.\d+)$")


def version_of(tag: str):
    """The version in a `vX.Y.Z` tag, or None if the tag does not have that form."""
    m = TAG.match(tag)
    return m.group(1) if m else None


def problems(tag: str, root: Path = None) -> list:
    root = root or ROOT
    version = version_of(tag)
    if version is None:
        return [f"{tag!r} is not a goldpan release tag: use vX.Y.Z"]
    found = []
    declared = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    if declared != version:
        found.append(f"pyproject.toml says version {declared}, the tag says {version}")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(rf"(?m)^## \[{re.escape(version)}\]", changelog):
        found.append(f"CHANGELOG.md has no section '## [{version}]' (rename [Unreleased] on the release branch)")
    return found


def main(argv) -> int:
    args = argv[1:]
    if len(args) == 2 and args[0] == "--version-only":
        version = version_of(args[1])
        if version is None:
            print(problems(args[1])[0], file=sys.stderr)
            return 1
        print(version)
        return 0
    if len(args) != 1:
        print(__doc__)
        return 2
    found = problems(args[0])
    for line in found:
        print(f"ERROR: {line}")
    if not found:
        print(f"{args[0]}: ready to publish goldpan {version_of(args[0])}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
