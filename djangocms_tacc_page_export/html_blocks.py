"""Turn HTML fragments (e.g. Text plugin bodies) into export blocks."""

from __future__ import annotations

import re
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString, Tag

from djangocms_tacc_page_export.document import Block

_HEADING_MAP = {
    'h1': 'heading1',
    'h2': 'heading2',
    'h3': 'heading3',
    'h4': 'heading3',
    'h5': 'heading3',
    'h6': 'heading3',
}

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

    blocks: list[Block] = []
    for block in _iter_blocks(root):
        blocks.extend(_blocks_for_element(block))
    return [block for block in blocks if block.text.strip()]


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
        return [Block('paragraph', collapse_whitespace(element.get_text(' ', strip=True)))]
    if name == 'a':
        href = (element.get('href') or '').strip()
        label = collapse_whitespace(element.get_text(' ', strip=True)) or href
        if href:
            return [Block('link_line', label, url=href)]
        return [Block('paragraph', label)] if label else []
    if name in ('ul', 'ol'):
        items = []
        for li in element.find_all('li', recursive=False):
            text = collapse_whitespace(li.get_text(' ', strip=True))
            if text:
                items.append(Block('bullet', text))
        return items
    text = collapse_whitespace(element.get_text(' ', strip=True))
    return [Block('paragraph', text)] if text else []
