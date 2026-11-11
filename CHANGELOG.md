# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases are tagged
`vX.Y.Z`.

## [Unreleased]

First pass over the book code itself, verifying each chapter against the
dependency ranges from 2.0.0 and fixing what no longer ran. Details are in
[docs/CONVERSION_NOTES.md](docs/CONVERSION_NOTES.md).

### Changed

- chapter04 no longer bundles `geolite2_city.mmdb`. MaxMind's GeoLite2 licence
  (EULA 6.3) forbids redistributing an outdated database, so `geo_ip.py`,
  `geo_print.py` and `google_earth_pcap.py` now take the database path with a
  `--db` option (default `geolite2_city.mmdb`) and print download instructions
  when it is missing. Removing the file shrinks a full checkout from ~100 MB to
  ~40 MB. The geoip2 4.8 API was verified against the scripts; no other change
  was needed.

### Fixed

- chapter03 `exif_fetch.py` called `Image._getexif()`, removed in Pillow 13. It
  now reads the GPSInfo sub-IFD with `getexif().get_ifd(...)`.
- chapter06 `anon_browser.py`: the `AnonBrowser` constructor raised
  `AttributeError` (it stored the user-agent pool under one name and read
  another), and `change_user_agent()` set an attribute MechanicalSoup ignores
  instead of calling `set_user_agent()`. Both are fixed, so the class works
  under MechanicalSoup 1.x.
- Invalid escape sequences (a `SyntaxWarning`, an error on Python 3.12+) in
  `chapter02/ssh_command.py`, `chapter03/discover_networks.py` and
  `chapter03/dump_recyclebin.py` are now raw strings with identical values.

### Tooling

- `tools/deps_scan.py` gained a `max_python` field (kept byte-identical with the
  blackhat-python3 copy) for dependencies with a Python ceiling.
- CI byte-compiles every chapter with `-W error::SyntaxWarning`.

## [2.0.0] - Unreleased

Modernizes the repository scaffolding: packaging, environments, CI and
documentation. **No book code under `chapterNN/` was changed.**

### Added

- `pyproject.toml` with one [PEP 735](https://peps.python.org/pep-0735/) dependency
  group per chapter, managed with [uv](https://docs.astral.sh/uv/), plus a committed
  `uv.lock`. Supports Python 3.11 to 3.14.
- `requirements/chNN.txt` for installing a single chapter with pip.
- Opt-in `ch05-bluetooth` group that builds PyBluez from a pinned upstream commit,
  because the last PyPI release no longer builds.
- `standard-crypt` backport so `chapter01/passwd_crack.py` keeps working on Python
  3.13+, where `crypt` was removed from the standard library (PEP 594). It is
  Unix-only, like the module it replaces.
- Dockerfile and a multi-arch image (`ghcr.io/eonraider/violent-python3`) with
  `nmap`, `tcpdump` and the BlueZ runtime. Images ship with SBOM and provenance
  attestations.
- Dev container configuration for GitHub Codespaces and local IDEs.
- `tools/deps_scan.py`: statically checks that every chapter's imports are declared
  in its dependency group, imports each dependency in CI, and generates the
  requirements files.
- GitHub Actions: an install matrix (Linux, macOS, Windows x Python 3.11-3.14), a
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
- Python 3.10 and older are no longer supported. 3.10 reached end of life in
  October 2026, and current security releases of some dependencies (Pillow 13,
  for example) require 3.11.

### Possibly breaking: dependency major versions

The 2020 pins don't install on current Python. Ranges were raised to the oldest
releases that do, and these crossed a major version or a large API boundary. Each
installs and imports cleanly in CI on every supported Python, but runtime
behaviour against the book code has not been verified yet:

| Package | Was | Now | Used by |
| --- | --- | --- | --- |
| `geoip2` | `~=3.0.0` | `>=4.8.1,<5` | chapter04 |
| `mechanicalsoup` | `~=0.12.0` | `>=1.3.0,<2` | chapter06 |
| `scapy` | `~=2.4.3` | `>=2.7.0,<3` (security fix) | chapter04, chapter05 |
| `pybluez` | `~=0.23` (PyPI) | upstream commit `82cbba8` | chapter05 (opt-in) |
| `requests` | `~=2.23.0` | `>=2.33.0` (security fixes) | chapter03 |

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

### Security

- Version floors no longer admit releases with known advisories:
  `pillow>=13.0.0` (chapter 3; earlier releases are affected by advisories fixed
  only in 13.0), `requests>=2.33.0` (chapter 3), `scapy>=2.7.0` (chapters 4 and 5;
  [GHSA-cq46-m9x9-j8w2](https://github.com/advisories/GHSA-cq46-m9x9-j8w2), code
  execution when loading an untrusted session file) and `pytest>=9.0.3` (dev). The
  lockfile moves `filelock`, a dependency of the `pre-commit` tooling, to 4.2.10.

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
