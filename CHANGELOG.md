# Changelog

All notable changes to goldpan. The format follows [Keep a Changelog](https://keepachangelog.com/), the versions follow [semantic versioning](https://semver.org/).

goldpan was the folder `python/` of [NSDF-Data](https://github.com/villano-lab/NSDF-Data) until 2026-11-05. Its history up to then is kept in this repository, and the changes of the releases made there (0.2.0 and 0.3.0) are in the `CHANGELOG.md` of NSDF-Data, on the lines that say `goldpan X.Y.Z`.

## [Unreleased]

### Changed

- **The `DCRC_RUN76` preset ends its pretrigger (baseline) window at 450 samples, not 500** (`goldpan.config`). The Run 76 trigger-locked pulses start at about sample 470 to 500 and a window ending at 500 let the rising edge into the baseline of some events, so `baseline_mean`, `baseline_std`, `current_max` and `integral` change a little. It follows the record `[readouts.DCRC_RUN76]` of the Run 76 registry (2026-11-02). Anything computed with the preset or its registry record should be computed again; code that gives its own `config` is not affected.

## [0.3.4] - 2026-11-06

The code is the code of 0.3.3 (only a docstring changed). This release publishes the guide pages of the documentation.

### Changed

- The guide *Writing an adapter* is a page of this documentation (`docs/guides/writing-an-adapter.md`); it was a quick-sheet of NSDF-Data. The batch-mode guide is in the goldsluice documentation.

## [0.3.3] - 2026-11-05

No change to the code: the package is the code of 0.3.2. This release carries the new documentation address in its metadata.

### Added

- The documentation of goldpan (Sphinx, `docs/`): how the pieces fit, guides, and the reference read from the docstrings, at https://villano-lab.github.io/goldpan/. A workflow builds it with warnings as errors for every pull request that touches `docs/`, `src/` or `pyproject.toml`, and deploys it to GitHub Pages when a release reaches `main` (or when run by hand). It replaces the pages `docs/api/` that NSDF-Data built from this package. The *Documentation* link of the package on PyPI points here from 0.3.3 (the releases before it keep the old NSDF-Data address, where a page now says the documentation moved).

## [0.3.2] - 2026-11-05

The environment check keeps working when goldpan is installed from PyPI (NSDF-Data pins it there from now on); no other function changed.

### Changed

- `check_environment` finds the `requirements.txt` of NSDF-Data by looking in the current folder and each folder above it (then above the module), so it works from a notebook, from `python -m check_environment` in the NSDF-Data folder, and when goldpan is installed from PyPI and no longer sits in the checkout. A file only counts if it names `nsdf-dark-matter`. New: `find_requirements()`, `--requirements FILE`, and `goldpan[extras]==X` lines are read by the package name.
- The test that wrote every `*.dataset.toml` of NSDF-Data back as the same definition looked for `goldsluice/examples` and `data_analysis` above this repository; it belongs to NSDF-Data and moved there.

## [0.3.1] - 2026-11-05

The first release made from this repository. The code is the same as 0.3.0 (the wheel was compared file by file with the one on PyPI: the same 34 files, the same contents); what changes is where goldpan lives and how it is published. `pip install goldpan` is unchanged.

### Added

- The tags `v0.2.0` and `v0.3.0` (the releases `goldpan-v0.2.0` and `goldpan-v0.3.0` of NSDF-Data, on the same commits of the kept history) and a GitHub Release for each.
- `LICENSE`, `CONTRIBUTING.md`, `AGENTS.md`, CI on Linux, Windows and macOS, and the publish workflow (`.github/workflows/publish-goldpan.yml`, `tools/check_release.py`): a tag `vX.Y.Z` builds the wheel and the source archive, tests the wheel in a clean environment and, after the maintainer approves the `pypi` environment, uploads with a trusted publisher.

### Changed

- goldpan is a repository of its own, `villano-lab/goldpan`, with the history of `python/`. The code is in `src/` (the package `goldpan` and the flat aliases `pulse_*.py`). Nothing in the package changed: the wheel has the same contents as 0.3.0.
- The tests of the tools, the notes, the registry data and the guides of NSDF-Data stay there (`tests/` of NSDF-Data); the tests of the library are in `tests/` here.

## [0.3.0] - 2026-11-04

The last release made from NSDF-Data. Dataset definition format 7 (a step can name its `sources`, steps build on each other, run metadata is joined at read time), `dataset.dump`, `registry.add_record`, `runmeta`, `rqdata` with `all_files=True`, and the 500-sample Run 76 readout. Details: the `goldpan 0.3.0` line of `CHANGELOG.md` in NSDF-Data, release 0.11.0.
