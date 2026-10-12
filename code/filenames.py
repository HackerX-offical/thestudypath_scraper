import re


def safe_image_filename(name: str, max_len: int = 120) -> str:
    cleaned = re.sub(r'[^\w\-_.]+', '_', name.strip())
    return cleaned[:max_len] or 'image'
