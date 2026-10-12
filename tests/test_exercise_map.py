import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from exercise_map import absolutize_url, classify_exercise_link  # noqa: E402


def test_classify_exercise_15a():
    assert classify_exercise_link('/exercise-15a/', 'Exercise 15A') == 'Exercise_15A'


def test_absolutize_relative():
    url = absolutize_url('https://www.thestudypath.com', '/page')
    assert url.endswith('/page')
