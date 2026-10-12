import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from config import BASE_URL, CHAPTER_15_INDEX  # noqa: E402


def test_chapter_url_on_domain():
    assert CHAPTER_15_INDEX.startswith(BASE_URL)
