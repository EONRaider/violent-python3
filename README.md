# Violent Python 3

[![CI](https://github.com/EONRaider/violent-python3/actions/workflows/ci.yml/badge.svg)](https://github.com/EONRaider/violent-python3/actions/workflows/ci.yml)
[![Python 3.11-3.14](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Managed with uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://docs.astral.sh/uv/)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/EONRaider/violent-python3)

The source code from **_Violent Python: A Cookbook for Hackers, Forensic Analysts,
Penetration Testers and Security Engineers_** by TJ O'Connor (Syngress, 2012),
converted from Python 2 to Python 3 and refactored to run on current interpreters
and libraries.

The scripts stay close to the printed listings so they can be read side by side with
the book. Every change made during the conversion is documented in
[docs/CONVERSION_NOTES.md](docs/CONVERSION_NOTES.md).

> [!NOTE]
> A companion conversion of _Black Hat Python_ by Justin Seitz lives at
> [EONRaider/blackhat-python3](https://github.com/EONRaider/blackhat-python3).

## Contents

- [Quick start](#quick-start)
- [Chapters](#chapters)
- [Downloading only what you need](#downloading-only-what-you-need)
- [Authorized use](#authorized-use)
- [Contributing](#contributing)
- [Translations](#translations)
- [License and credits](#license-and-credits)

## Quick start

Python 3.11 or newer. Pick one of the following setups.

### uv (recommended)

[uv](https://docs.astral.sh/uv/getting-started/installation/) installs the right
Python version if you don't have it and reproduces the exact dependency versions
tested in CI from `uv.lock`.

```shell
git clone https://github.com/EONRaider/violent-python3.git
cd violent-python3
uv sync                              # every chapter
uv run python chapter04/geo_ip.py -h
```

Each chapter is a separate [dependency group](https://peps.python.org/pep-0735/), so you
can install only what you are reading:

```shell
uv sync --only-group ch04            # just chapter 4
uv sync --group ch05-bluetooth       # add the opt-in Bluetooth extras (Linux)
```

### pip

```shell
git clone https://github.com/EONRaider/violent-python3.git
cd violent-python3
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt      # every chapter
pip install -r requirements/ch04.txt # or just one chapter
```

`requirements*.txt` carry version ranges. For the exact versions tested in CI, use
`requirements-lock.txt` (and `requirements-lock-bluetooth.txt` for the opt-in group)
from the [latest release](https://github.com/EONRaider/violent-python3/releases/latest).
With pip 25.1 or newer, you can also install a chapter's group straight from
`pyproject.toml` with `pip install --group ch04`.

### Docker

Each [release](https://github.com/EONRaider/violent-python3/releases) publishes an
image for `linux/amd64` and `linux/arm64` with every chapter's dependencies, `nmap`,
`tcpdump` and the BlueZ runtime preinstalled:

```shell
docker run --rm -it ghcr.io/eonraider/violent-python3
# Chapters that sniff or forge packets need raw-socket capabilities:
docker run --rm -it --cap-add=NET_RAW --cap-add=NET_ADMIN ghcr.io/eonraider/violent-python3
# Or build it yourself:
docker build -t violent-python3 . && docker run --rm -it violent-python3
```

The image runs as `root` because most raw-socket chapters need it. With only the
capabilities above, the container still isolates those scripts from the host, so
add just what a chapter needs. Bluetooth (chapter 5) is different: it needs the
host's network namespace to reach the adapter, for example with
`--net=host --cap-add=NET_RAW --cap-add=NET_ADMIN`. That **removes network
isolation**, so the container can see and act on all host traffic. Avoid
`--privileged`, which also gives the container access to every host device.

### GitHub Codespaces / Dev Containers

Use the **Open in GitHub Codespaces** badge above, or open the folder in VS Code or
JetBrains with the Dev Containers extension. The container
([.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)) has the same tools
as the Docker image, plus `uv`, `git` and compilers, and comes with raw-socket
capabilities already granted.

### System packages

Some chapters call external programs or need native libraries. The Docker image and
dev container already include them; on a host install them yourself:

| Needed for | Debian / Ubuntu / Kali | macOS (Homebrew) |
| --- | --- | --- |
| `chapter02/nmap_scan.py`, `conficker.py` | `apt install nmap` | `brew install nmap` |
| Packet capture (chapters 4-5) | `apt install libpcap0.8 tcpdump` | built in |
| `ch05-bluetooth` group | `apt install libbluetooth-dev` | not supported |

## Chapters

| Chapter | Topic | `uv` group | PyPI packages | Notes |
| --- | --- | --- | --- | --- |
| [01](chapter01) | Introduction | `ch01` | `standard-crypt` (not Windows, Python 3.13+) | `crypt` was removed from the stdlib in 3.13 ([PEP 594](https://peps.python.org/pep-0594/)); the backport keeps `passwd_crack.py` working. Like the original module it wraps libc `crypt(3)`, so `passwd_crack.py` does not run on Windows. |
| [02](chapter02) | Penetration testing | `ch02` | `pexpect`, `python-nmap` | `nmap` binary required. Uses SSH and FTP against hosts you control. |
| [03](chapter03) | Forensic investigations | `ch03` | `beautifulsoup4`, `pillow`, `pypdf4`, `requests` | `discover_networks.py` and `dump_recyclebin.py` read the Windows registry and need Windows with Administrator rights. Sample Firefox/Skype databases and a PDF are included. |
| [04](chapter04) | Network traffic analysis | `ch04` | `dpkt`, `geoip2`, `ipy`, `scapy` | Sample `.pcap` files are included. The GeoLite2 City database is **not** bundled (MaxMind's licence forbids redistributing an outdated copy); the `geo_*.py` scripts take its path with `--db` — see [NOTICE](NOTICE). Live sniffing needs root / `NET_RAW`. |
| [05](chapter05) | Wireless mayhem | `ch05`, `ch05-bluetooth` | `scapy`, `pybluez` (Linux, opt-in) | Wi-Fi scripts need a card in monitor mode. `ninja_print.py` needs the ObexFTP Python 2 bindings, which have no Python 3 port. |
| [06](chapter06) | Web reconnaissance | `ch06` | `beautifulsoup4`, `mechanicalsoup` | The Google and Twitter scripts target APIs that no longer exist; see the conversion notes. |
| [07](chapter07) | Antivirus evasion | - | - | Standard library only. |

The PyPI column is generated by `python tools/deps_scan.py report`, which reads the
imports in each chapter. The OS and privilege notes come from the conversion notes
and may be incomplete; corrections are welcome.

## Downloading only what you need

A full checkout is about 40 MB, mostly sample data: the largest single file is a
30 MB archive of weak Debian SSH keys in `chapter02/`. Shallow clones
(`--depth 1`) save very little because that file is part of the current tree. To
download just the chapters you want:

```shell
git clone --filter=blob:none --sparse https://github.com/EONRaider/violent-python3.git
cd violent-python3
git sparse-checkout set chapter01 chapter03    # any chapters you want
```

Or skip cloning entirely and use the [Docker image](#docker).

## Authorized use

This code performs real attacks: password cracking, SSH brute forcing, packet
injection, wireless and Bluetooth exploitation. Run it only against systems you own
or have written permission to test.

## Contributing

Bug fixes, compatibility fixes for newer libraries and documentation improvements are
welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the scope, the development
workflow and how releases are cut. Report security issues as described in
[SECURITY.md](SECURITY.md).

## Translations

- Turkish, by [Bedirhan Budak](https://github.com/bedirhanbudak): [`turkish-language` branch](https://github.com/EONRaider/violent-python3/tree/turkish-language)

## License and credits

The code is derived from _Violent Python_ by TJ O'Connor, published by Syngress, an
imprint of Elsevier, Inc. **No open-source license is granted**; see [NOTICE](NOTICE) for what
that means and for the terms of the bundled third-party files. The Python 3 conversion
is by [EONRaider](https://github.com/EONRaider) and
[contributors](https://github.com/EONRaider/violent-python3/graphs/contributors).

If you reference this repository in academic work, GitHub's **Cite this repository**
button uses [CITATION.cff](CITATION.cff).
