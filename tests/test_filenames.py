import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from filenames import safe_image_filename  # noqa: E402


def test_safe_image_filename_strips_bad_chars():
    assert safe_image_filename('Q 1 / part (a)') == 'Q_1_part_a_'
