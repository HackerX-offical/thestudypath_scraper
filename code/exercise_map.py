from __future__ import annotations

from urllib.parse import urljoin


def classify_exercise_link(href: str, text: str) -> str | None:
    href_l = href.lower()
    text_l = text.lower()
    if 'exercise-15a' in href_l or 'exercise-15a' in text_l:
        return 'Exercise_15A'
    if 'exercise-15b' in href_l or 'exercise-15b' in text_l:
        return 'Exercise_15B'
    if 'exercise-15c' in href_l or 'exercise-15c' in text_l:
        return 'Exercise_15C'
    if 'exercise-15d' in href_l or 'exercise-15d' in text_l:
        return 'Exercise_15D'
    if 'multiple-choice' in href_l or 'mcq' in href_l:
        return 'MCQs'
    return None


def absolutize_url(base_url: str, url: str) -> str:
    if url.startswith('http'):
        return url
    return urljoin(base_url, url)
