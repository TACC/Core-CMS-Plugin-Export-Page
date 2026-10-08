"""Public export API."""

from __future__ import annotations

import io
import re
import zipfile
from typing import Iterable

from djangocms_tacc_page_export.collector import page_document_for_draft_page
from djangocms_tacc_page_export.docx_writer import write_page_document
_FILENAME_SAFE_RE = re.compile(r'[^a-zA-Z0-9._-]+')


def slug_for_filename(page, language: str | None = None) -> str:
    draft = page.get_draft_object() if hasattr(page, 'get_draft_object') else page
    try:
        slug = draft.get_slug(language) or ''
    except Exception:
        slug = getattr(draft, 'slug', '') or ''
    slug = slug.strip('/') or 'page'
    return _FILENAME_SAFE_RE.sub('-', slug).strip('-') or 'page'


def export_page_to_docx(page, language: str | None = None) -> bytes:
    document = page_document_for_draft_page(page, language=language)
    return write_page_document(document)


def export_pages_to_docx_files(
    pages: Iterable,
    language: str | None = None,
) -> list[tuple[str, bytes]]:
    files: list[tuple[str, bytes]] = []
    for page in pages:
        document = page_document_for_draft_page(page, language=language)
        filename = f'{slug_for_filename(page, language)}.docx'
        files.append((filename, write_page_document(document)))
    return files


def zip_docx_files(files: list[tuple[str, bytes]]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in files:
            archive.writestr(name, payload)
    return buffer.getvalue()


def export_pages_download(
    pages: Iterable,
    language: str | None = None,
) -> tuple[str, str, bytes]:
    """Return ``(filename, content_type, payload)`` for an HTTP download."""
    page_list = list(pages)
    if not page_list:
        raise ValueError('No pages to export')
    if len(page_list) == 1:
        page = page_list[0]
        filename = f'{slug_for_filename(page, language)}.docx'
        return (
            filename,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            export_page_to_docx(page, language=language),
        )
    files = export_pages_to_docx_files(page_list, language=language)
    return (
        'pages-export.zip',
        'application/zip',
        zip_docx_files(files),
    )
