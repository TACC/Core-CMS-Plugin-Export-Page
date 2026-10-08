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
class Block:
    kind: BlockKind
    text: str
    url: Optional[str] = None


@dataclass
class PageDocument:
    title: str
    blocks: list[Block] = field(default_factory=list)
    slug: str = ''
    page_url: str = ''
