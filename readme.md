# thestudypath_scraper

Python scraper for StudyPath chapter exercise images and PDF assembly.

## Why this exists

Educational content archival for accounts you own can be automated with resumable downloads and PDF bundling.

## Features

- Scraper under `code/`
- Generated PDFs under `pdfs/`
- CI pytest gate

## Install

```bash
git clone https://github.com/HackerX-offical/thestudypath_scraper.git
cd thestudypath_scraper
pip install -r requirements.txt
```

## Quick start

```bash
python3 code/main.py
```

## Output

Images and PDFs under `pdfs/` per chapter.

## Develop

```bash
pytest tests -q
```

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for module layout and extension points.

## Ethics

Use only on systems and content you are **authorized** to test. See [SECURITY.md](./SECURITY.md).

## License

Licensed under the [HackerX License](./LICENSE). Redistributions must retain copyright,
license text, and [NOTICE](./NOTICE) attribution per the license terms.
