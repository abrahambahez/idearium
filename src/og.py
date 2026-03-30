import re


def extract_og_description(body: str, max_len: int = 160) -> str:
    text = re.sub(r'^#{1,6}\s+', '', body, flags=re.MULTILINE)
    text = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_\n]+)_{1,3}', r'\1', text)
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)
    text = ' '.join(text.split())
    if not text:
        return ''
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(' ', 1)[0]
    return cut + '…'
