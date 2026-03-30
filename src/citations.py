import html
import json
import os
import re
from pathlib import Path

# Matches a full Pandoc-style citation block: [...] containing at least one @key
CITATION_BLOCK_RE = re.compile(r'\[([^\[\]]*@[\w:-][^\[\]]*)\]')
# Extracts individual citekeys within a block
KEY_RE = re.compile(r'@([\w:-]+)')


def _format_authors(authors: list[dict]) -> str:
    if not authors:
        return ""
    names = []
    for i, a in enumerate(authors):
        if "literal" in a:
            names.append(a["literal"])
        elif "family" in a:
            given = a.get("given", "")
            if i == 0:
                names.append(f"{a['family']}, {given}".strip(", "))
            else:
                names.append(f"{given} {a['family']}".strip())
        elif "given" in a:
            names.append(a["given"])
    if len(names) > 3:
        return f"{names[0]} et al."
    return "; ".join(names)


def _format_year(entry: dict) -> str:
    parts = entry.get("issued", {}).get("date-parts", [[]])
    if parts and parts[0]:
        return str(parts[0][0])
    return "s.f."


def _format_identifier(entry: dict) -> str:
    if entry.get("DOI"):
        return f"DOI: {entry['DOI']}"
    if entry.get("ISBN"):
        return f"ISBN: {entry['ISBN']}"
    if entry.get("URL"):
        return f"URL: {entry['URL']}"
    return ""


def _format_editors(editors: list[dict]) -> str:
    if not editors:
        return ""
    names = []
    for e in editors:
        if "literal" in e:
            names.append(e["literal"])
        elif "family" in e:
            given = e.get("given", "")
            names.append(f"{given} {e['family']}".strip())
    return "; ".join(names)


def _format_ref(entry: dict) -> str:
    t = entry.get("type", "document")
    title = entry.get("title") or "[no title]"
    authors = _format_authors(entry.get("author", []))
    year = _format_year(entry)
    publisher = entry.get("publisher", "")
    identifier = _format_identifier(entry)

    def parts(*items) -> str:
        return " ".join(x for x in items if x)

    if t == "article-journal":
        journal = entry.get("container-title", "")
        vol = entry.get("volume", "")
        issue = entry.get("issue", "")
        page = entry.get("page", "")
        vol_issue = f"{vol}({issue})" if vol and issue else vol or issue
        page_str = f"pp. {page}" if page else ""
        return parts(
            f"{authors}." if authors else "",
            f'"{title}."',
            f"{journal}" + (f" {vol_issue}," if vol_issue else ",") if journal else "",
            f"{year}.",
            page_str + ("." if page_str else ""),
            identifier,
        )

    if t == "book":
        return parts(
            f"{authors}." if authors else "",
            f"{title}.",
            f"{publisher}," if publisher else "",
            f"{year}.",
            identifier,
        )

    if t == "chapter":
        container = entry.get("container-title", "")
        editors = _format_editors(entry.get("editor", []))
        page = entry.get("page", "")
        page_str = f"pp. {page}" if page else ""
        ed_str = f"ed. {editors}" if editors else ""
        return parts(
            f"{authors}." if authors else "",
            f'"{title}."',
            f"In {container}," if container else "",
            f"{ed_str}." if ed_str else "",
            f"{publisher}," if publisher else "",
            f"{year}.",
            page_str + ("." if page_str else ""),
            identifier,
        )

    if t == "thesis":
        return parts(
            f"{authors}." if authors else "",
            f"{title}.",
            "[Thesis].",
            f"{publisher}," if publisher else "",
            f"{year}.",
            identifier,
        )

    if t == "paper-conference":
        event = entry.get("event", "")
        return parts(
            f"{authors}." if authors else "",
            f'"{title}."',
            f"{event}." if event else "",
            f"{publisher}," if publisher else "",
            f"{year}.",
            identifier,
        )

    # document, article-magazine, article-newspaper, others
    return parts(
        f"{authors}." if authors else "",
        f'"{title}."',
        f"{publisher}," if publisher else "",
        f"{year}.",
        identifier,
    )


def load_refs() -> dict[str, str]:
    """Return {citekey: formatted_ref_string} for all entries in LIBRARY_FILE."""
    lib_path = os.environ.get("LIBRARY_FILE")
    if not lib_path:
        raise RuntimeError("LIBRARY_FILE environment variable is not set")
    path = Path(lib_path).expanduser()
    if not path.exists():
        raise RuntimeError(f"LIBRARY_FILE not found: {path}")
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)
    return {e["id"]: _format_ref(e) for e in entries if "id" in e}


def preprocess_citations(text: str, refs: dict[str, str]) -> str:
    """Replace Pandoc-style citation blocks with <span class="cite"> HTML.
    Handles [@key], [@key, p. 7], and [@key1; @key2]. Unknown keys are left intact."""
    def _replace(m: re.Match) -> str:
        keys = KEY_RE.findall(m.group(1))
        found = []
        for key in keys:
            ref = refs.get(key)
            if ref is None:
                print(f"  [citations] unknown citekey: {key}", flush=True)
            else:
                found.append(ref)
        if not found:
            return m.group(0)
        safe_refs = html.escape(json.dumps(found), quote=True)
        return f'<span class="cite" data-refs="{safe_refs}">{m.group(0)}</span>'
    return CITATION_BLOCK_RE.sub(_replace, text)
