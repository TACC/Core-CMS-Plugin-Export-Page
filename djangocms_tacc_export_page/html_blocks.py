"""Turn HTML fragments (e.g. Text plugin bodies) into export blocks."""

from __future__ import annotations

import re
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString, Tag

from djangocms_tacc_export_page.document import Block, InlineSpan

_HEADING_MAP = {
    'h1': 'heading1',
    'h2': 'heading2',
    'h3': 'heading3',
    'h4': 'heading3',
    'h5': 'heading3',
    'h6': 'heading3',
}

# Block-level tags that should split export into multiple DOCX blocks.
_FLOW_BREAKING_TAGS = frozenset(
    _HEADING_MAP.keys()
    | {'p', 'ul', 'ol', 'li', 'pre', 'blockquote', 'table', 'hr', 'dl', 'dt', 'dd'}
)

_WHITESPACE_RE = re.compile(r'\s+')


def collapse_whitespace(text: str) -> str:
    return _WHITESPACE_RE.sub(' ', (text or '').strip())


def html_to_blocks(html: str) -> list[Block]:
    if not html or not str(html).strip():
        return []

    soup = BeautifulSoup(f'<div data-export-root>{html}</div>', 'lxml')
    root = soup.select_one('div[data-export-root]')
    if not root:
        return []

    if not _has_flow_breaking_descendant(root):
        text = collapse_whitespace(root.get_text(' ', strip=True))
        if not text:
            return []
        return [
            Block(
                'paragraph',
                text,
                runs=_inline_runs(root),
            )
        ]

    blocks: list[Block] = []
    for block in _iter_blocks(root):
        blocks.extend(_blocks_for_element(block))
    return [block for block in blocks if _block_has_content(block)]


def _block_has_content(block: Block) -> bool:
    if block.runs:
        return bool(collapse_whitespace(''.join(span.text for span in block.runs)))
    return bool(block.text.strip())


def _has_flow_breaking_descendant(root: Tag) -> bool:
    for element in root.descendants:
        if isinstance(element, Tag) and element.name in _FLOW_BREAKING_TAGS:
            return True
    return False


def _iter_blocks(root: Tag) -> Iterable[Tag]:
    for child in root.children:
        if isinstance(child, NavigableString):
            text = collapse_whitespace(str(child))
            if text:
                yield _pseudo_paragraph(text)
            continue
        if not isinstance(child, Tag):
            continue
        if child.name in _HEADING_MAP or child.name in ('p', 'ul', 'ol'):
            yield child
            continue
        if child.name == 'a' and child.get('href'):
            yield child
            continue
        if child.name in ('div', 'section', 'article', 'main', 'span'):
            yield from _iter_blocks(child)
            continue
        text = collapse_whitespace(child.get_text(' ', strip=True))
        if text:
            yield _pseudo_paragraph(text)


def _pseudo_paragraph(text: str) -> Tag:
    soup = BeautifulSoup(f'<p>{text}</p>', 'lxml')
    return soup.find('p')


def _paragraph_block(element: Tag) -> Block:
    text = collapse_whitespace(element.get_text(' ', strip=True))
    return Block('paragraph', text, runs=_inline_runs(element))


def _blocks_for_element(element: Tag) -> list[Block]:
    name = element.name
    if name in _HEADING_MAP:
        return [
            Block(
                _HEADING_MAP[name],
                collapse_whitespace(element.get_text(' ', strip=True)),
            )
        ]
    if name == 'p':
        return [_paragraph_block(element)]
    if name == 'a':
        href = (element.get('href') or '').strip()
        label = collapse_whitespace(element.get_text(' ', strip=True)) or href
        if href:
            return [Block('link_line', label, url=href)]
        return [_paragraph_block(element)] if label else []
    if name in ('ul', 'ol'):
        items = []
        for li in element.find_all('li', recursive=False):
            if not _block_has_content(_paragraph_block(li)):
                continue
            block = _paragraph_block(li)
            items.append(Block('bullet', block.text, runs=block.runs))
        return items
    text = collapse_whitespace(element.get_text(' ', strip=True))
    return [Block('paragraph', text, runs=_inline_runs(element))] if text else []


def _inline_runs(root: Tag) -> tuple[InlineSpan, ...]:
    runs: list[InlineSpan] = []

    def append_text(
        text: str,
        *,
        bold: bool,
        italic: bool,
        code: bool,
        url: str | None,
    ) -> None:
        normalized = _WHITESPACE_RE.sub(' ', text)
        if not normalized:
            return
        runs.append(
            InlineSpan(
                text=normalized,
                bold=bold,
                italic=italic,
                code=code,
                url=url,
            )
        )

    def walk(
        node,
        *,
        bold: bool = False,
        italic: bool = False,
        code: bool = False,
        url: str | None = None,
    ) -> None:
        if isinstance(node, NavigableString):
            append_text(str(node), bold=bold, italic=italic, code=code, url=url)
            return
        if not isinstance(node, Tag):
            return
        name = node.name
        if name == 'br':
            append_text(' ', bold=bold, italic=italic, code=code, url=url)
            return
        if name in ('strong', 'b'):
            for child in node.children:
                walk(child, bold=True, italic=italic, code=code, url=url)
            return
        if name in ('em', 'i'):
            for child in node.children:
                walk(child, bold=bold, italic=True, code=code, url=url)
            return
        if name == 'code':
            for child in node.children:
                walk(child, bold=bold, italic=italic, code=True, url=url)
            return
        if name == 'a':
            href = (node.get('href') or '').strip() or None
            for child in node.children:
                walk(child, bold=bold, italic=italic, code=code, url=href or url)
            return
        for child in node.children:
            walk(child, bold=bold, italic=italic, code=code, url=url)

    for child in root.children:
        walk(child)

    return _merge_runs(runs)


def _merge_runs(runs: list[InlineSpan]) -> tuple[InlineSpan, ...]:
    if not runs:
        return ()
    merged: list[InlineSpan] = [runs[0]]
    for span in runs[1:]:
        previous = merged[-1]
        if (
            previous.bold == span.bold
            and previous.italic == span.italic
            and previous.code == span.code
            and previous.url == span.url
        ):
            merged[-1] = InlineSpan(
                previous.text + span.text,
                bold=previous.bold,
                italic=previous.italic,
                code=previous.code,
                url=previous.url,
            )
        else:
            merged.append(span)
    return tuple(merged)
