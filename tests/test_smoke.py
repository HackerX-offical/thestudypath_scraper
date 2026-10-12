from pathlib import Path


def test_scraper_code_exists():
    root = Path(__file__).resolve().parents[1]
    py_files = list((root / "code").glob("**/*.py"))
    assert py_files, "expected Python sources under code/"
