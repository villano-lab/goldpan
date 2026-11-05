# AGENTS.md: working in goldpan

Instructions for AI coding agents (Claude Code, Codex, Copilot, Cursor and others) and for human contributors. `CLAUDE.md` points here. The Git rules are in `CONTRIBUTING.md`; read it too.

## What this repository is

goldpan is the pulse-analysis library of the NSDF-Data project (SuperCDMS-type detector data, Run 76): operations on traces, cuts, derived quantities, readers and writers (adapters) for the data formats, the dataset definition format and the detector registry reader. It was the folder `python/` of https://github.com/villano-lab/NSDF-Data until 2026-11-05.

- `src/goldpan/`: the package. `src/pulse_*.py` are the flat names of the first versions, thin aliases of the package (`goldpan.legacy`), kept for the existing notebooks and to be removed. `src/check_environment.py` is the environment check that NSDF-Data's first-analysis guide imports.
- `tests/`: the tests of the library. `tests/data/` and `tests/synthetic_series.py` are small made-up data; there is no detector data in this repository.
- `tools/check_release.py`: the release checker the publish workflow runs.

What is **not** here, and stays in NSDF-Data: the detector registry (`registry/`: data, not code, to become repositories of its own), the analysis notebooks (`data_analysis/`), the student guides and notes, and the reduction package `goldsluice/`, which depends on goldpan. **Nothing in goldpan may depend on any of them.**

The maintainer is Anthony Villano (@villaa).

## Before you change anything

1. `git status` and `git log --oneline -3`. Pull first. Be on a `feature/*` branch made from an up-to-date `develop`.
2. `python -m pip install -e ".[archive,parquet,root,midas]" pytest`, then `python -m pytest -q` (all of it passes; a test is skipped only when a dependency is missing).
3. **One working copy per session.** If `git status` shows changes you did not make, or another session may be using this folder, do not touch them: make your own worktree (`git worktree add ../goldpan-<task> -b feature/<name> origin/develop`) and remove it when done.

## Rules

- Branches and merging: `CONTRIBUTING.md`. Never commit to `main` or `develop`, never force-push, merge commits only. **An agent never merges a pull request without the maintainer's explicit go-ahead, and never pushes a release tag (`vX.Y.Z`): it publishes to PyPI, which cannot be undone.**
- A line under `[Unreleased]` in `CHANGELOG.md` for any change a user would notice. Only a `release/*` or `hotfix/*` branch changes the version.
- Write commit messages that say what changed and why. If an AI assistant helped, add a `Co-Authored-By:` trailer naming it.
- Never commit raw data, credentials or tokens.
- Every public function has `@status(DONE)` or `@status(UNDER_DEVELOPMENT, note=...)` and is mentioned in a test.
- A new key of the dataset definition (`src/goldpan/dataset.py`, whose docstring is the specification) raises `FORMAT_VERSION`, updates the docstring and gets a test in `tests/test_goldpan_dataset.py`. Unknown keys are refused on purpose: do not make the reader lenient. Same for the registry reader (`registry.py`): a new key raises its `FORMAT_VERSION`; a name defined twice is an error on purpose.
- A fix that changes what an existing adapter returns for the same file raises its `REVISION` by one in the same pull request (`goldsluice run` then redoes the outputs made with it).
- A breaking change (a rename or removal) is announced in `CHANGELOG.md`, and the notebooks of NSDF-Data that use the name are updated or marked deprecated there.

## Analysis pitfalls

- **The readout is never assumed.** `goldpan.config.PulseConfig` has no defaults and every function takes a `config`. The Run 76 readout (`DCRC_RUN76`: 0.8 us per sample, 1.25 MHz, a 4096-sample trace is 3.2768 ms, baseline window of 500 samples) and Z7 (1.6 us, 625 kHz) are kept as presets for old code; they are to be dropped, and every analysis is to take its readout from its detector registry.
- The channel names depend on the readout. Run 76 (this series) is Side-2 readout: six sensors, all on Side 2 (`Side2pA` to `Side2pF`); DCRC4 pA (dump channel (2, 0)) is the NaI trigger input. Never assume a `Side1p...` channel exists in it.
- A trace's first ~10 samples can carry an electronics glitch of hundreds of counts. Skip `config.glitch_samples` (or use `operations.trim_glitch`) before any full-trace operation such as an FFT.
- Event numbers restart in every dump, so they are not globally unique. A *segment* is a stretch of consecutive same-trigger-type events; a *run* is a whole data-taking period.
- The `randoms` / `real_triggers` cuts rest on an unconfirmed assumption that the `.csv` trigger labels are swapped; they are tagged under development for that reason.
- Raw dump data lives outside any repository (`~/idx`); never put it here.
