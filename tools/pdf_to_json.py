import json
import os
import re
from typing import List, Dict, Literal

from pypdf import PdfReader


Language = Literal["english", "hindi"]


def read_pdf_text_per_page(pdf_path: str) -> List[str]:
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    reader = PdfReader(pdf_path)
    pages_text: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)
    return pages_text


def split_into_sections(text: str, language: Language) -> List[Dict[str, str]]:
    # Heuristic regex per language; fallback to single chunk if no match
    if language == "english":
        # Matches: Section 1, SECTION 2, Sec. 3, etc.
        pattern = r"(?:\n|\A)\s*(?:Section|Sec\.)\s*(\d+[A-Z]?)\s*[:.-]?\s"  # captures section number
    else:
        # Hindi: धारा 1 / धारा 1A etc.
        pattern = r"(?:\n|\A)\s*धारा\s*(\d+[A-Z]?)\s*[:.-]?\s"

    parts: List[Dict[str, str]] = []
    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
    if not matches:
        return []

    for i, match in enumerate(matches):
        start = match.start()
        section_id = match.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk = text[start:end].strip()
        parts.append({
            "section": section_id,
            "content": chunk
        })
    return parts


def pdf_to_json(
    pdf_path: str,
    output_json_path: str,
    language: Language,
    mode: Literal["sections", "pages"] = "sections",
) -> List[Dict[str, str]]:
    pages = read_pdf_text_per_page(pdf_path)

    records: List[Dict[str, str]] = []

    if mode == "sections":
        # Join all pages and attempt section-based split
        full_text = "\n".join(pages)
        sections = split_into_sections(full_text, language)
        if sections:
            for item in sections:
                records.append({
                    "id": f"{language}_sec_{item['section']}",
                    "language": language,
                    "granularity": "section",
                    "section": item["section"],
                    "text": item["content"],
                })
        else:
            # Fallback to pages if no sections found
            mode = "pages"

    if mode == "pages":
        for idx, text in enumerate(pages):
            text = (text or "").strip()
            if not text:
                continue
            records.append({
                "id": f"{language}_page_{idx+1}",
                "language": language,
                "granularity": "page",
                "page": idx + 1,
                "text": text,
            })

    os.makedirs(os.path.dirname(output_json_path) or ".", exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return records


if __name__ == "__main__":
    # Defaults for quick local run
    pdf_to_json("ipc_section_english.pdf", "ipc_english.json", language="english", mode="sections")
    pdf_to_json("ipc_section_hindi.pdf", "ipc_hindi.json", language="hindi", mode="sections")
    print("Exported ipc_english.json and ipc_hindi.json")



