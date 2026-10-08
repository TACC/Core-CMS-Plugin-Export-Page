"""Intermediate document model between CMS plugins and DOCX."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

BlockKind = Literal[
    'heading1',
    'heading2',
    'heading3',
    'paragraph',
    'bullet',
    'link_line',
]


@dataclass(frozen=True)
class InlineSpan:
    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False
    url: Optional[str] = None


@dataclass(frozen=True)
class Block:
    kind: BlockKind
    text: str
    url: Optional[str] = None
    runs: tuple[InlineSpan, ...] = ()


@dataclass
class PageDocument:
    title: str
    blocks: list[Block] = field(default_factory=list)
    slug: str = ''
    page_url: str = ''
