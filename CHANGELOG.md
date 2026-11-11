# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases are tagged
`vX.Y.Z`.

## [Unreleased]

## [2.0.0] - Unreleased

Modernizes the repository scaffolding: packaging, environments, CI and
documentation. **No book code under `chapterNN/` was changed.**

### Added

- `pyproject.toml` with one [PEP 735](https://peps.python.org/pep-0735/) dependency
  group per chapter, managed with [uv](https://docs.astral.sh/uv/), plus a committed
  `uv.lock`. Supports Python 3.10 to 3.14.
- `requirements/chNN.txt` for installing a single chapter with pip.
- Opt-in `ch05-bluetooth` group that builds PyBluez from a pinned upstream commit,
  because the last PyPI release no longer builds.
- `standard-crypt` backport so `chapter01/passwd_crack.py` keeps working on Python
  3.13+, where `crypt` was removed from the standard library (PEP 594).
- Dockerfile and a multi-arch image (`ghcr.io/eonraider/violent-python3`) with
  `nmap`, `tcpdump` and the BlueZ runtime. Images ship with SBOM and provenance
  attestations.
- Dev container configuration for GitHub Codespaces and local IDEs.
- `tools/deps_scan.py`: statically checks that every chapter's imports are declared
  in its dependency group, imports each dependency in CI, and generates the
  requirements files.
- GitHub Actions: an install matrix (Linux, macOS, Windows x Python 3.10-3.14), a
  Docker build, link checking, Markdown lint, actionlint and zizmor. Every action is
  pinned to a commit SHA.
- Dependabot for uv, GitHub Actions, Docker and dev containers.
- `NOTICE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1),
  `SECURITY.md`, `CITATION.cff`, issue forms and a pull request template.

### Changed

- The README was rewritten with setup instructions for uv, pip, Docker and
  Codespaces, and a chapter table. The conversion notes moved, otherwise unchanged,
  to `docs/CONVERSION_NOTES.md`.
- `requirements.txt` is now generated from `pyproject.toml`
  (`python tools/deps_scan.py requirements`). It lists version ranges, and each
  release attaches a pinned `requirements-lock.txt`.
- Python 3.9 and older are no longer supported. 3.9 reached end of life in
  October 2025.

### Possibly breaking: dependency major versions

The 2020 pins don't install on current Python. Ranges were raised to the oldest
releases that do, and these crossed a major version or a large API boundary. Each
installs and imports cleanly in CI on every supported Python, but runtime
behaviour against the book code has not been verified yet:

| Package | Was | Now | Used by |
| --- | --- | --- | --- |
| `geoip2` | `~=3.0.0` | `>=4.8.1,<5` | chapter04 |
| `mechanicalsoup` | `~=0.12.0` | `>=1.3.0,<2` | chapter06 |
| `scapy` | `~=2.4.3` | `>=2.6.1,<3` | chapter04, chapter05 |
| `pybluez` | `~=0.23` (PyPI) | upstream commit `82cbba8` | chapter05 (opt-in) |
| `requests` | `~=2.23.0` | `>=2.32.4` (security fixes) | chapter03 |

### Removed

- Poetry configuration (`poetry.lock` and the Poetry `pyproject.toml`), which had
  placeholder author metadata and an 80 % coverage gate that no test could reach.
- The placeholder `tests/` tree and `CHANGELOG_ENTRY.md`, superseded by
  `tools/tests/` and this file.
- Explicit pins of transitive dependencies (`ptyprocess`), now resolved by the
  lockfile.

### Fixed

- The PyBluez environment marker was `sys_platform == 'darwin'`. PyBluez targets
  Linux (BlueZ), so the marker is now `sys_platform == 'linux'`.

## Before 2.0.0

The Python 3 conversion itself (2020) and later fixes are recorded in the git
history. Notable items:

- Converted all chapters to Python 3 and PEP 8, replacing `optparse` with
  `argparse` and file handling with context managers.
- Fixed file positions not being reset between reads when one file object was
  passed to several functions.
- Raised Pillow to 8.3.2 for security fixes.
- Added the Turkish translation (`turkish-language` branch).

[Unreleased]: https://github.com/EONRaider/violent-python3/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/EONRaider/violent-python3/releases/tag/v2.0.0
