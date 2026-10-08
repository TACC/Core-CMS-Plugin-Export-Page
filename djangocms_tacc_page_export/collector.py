"""Walk a CMS placeholder plugin tree and collect export blocks."""

from __future__ import annotations

from dataclasses import dataclass, field

from django.conf import settings

from djangocms_tacc_page_export.document import Block, PageDocument
from djangocms_tacc_page_export.plugin_readers.registry import read_plugin


@dataclass
class CollectorContext:
    language: str
    blocks: list[Block] = field(default_factory=list)

    def extend(self, new_blocks: list[Block]) -> None:
        self.blocks.extend(new_blocks)

    def read_children(self, plugin) -> None:
        for child in plugin.get_children().order_by('position'):
            read_plugin(child, self)


def collect_placeholder_plugins(placeholder, language: str | None = None) -> list[Block]:
    language = language or settings.LANGUAGE_CODE
    context = CollectorContext(language=language)
    for plugin in placeholder.get_plugins(language).filter(parent__isnull=True):
        read_plugin(plugin, context)
    return context.blocks


def page_document_for_draft_page(page, language: str | None = None) -> PageDocument:
    """Build a document from the draft page's ``content`` placeholder."""
    language = language or settings.LANGUAGE_CODE
    draft = page.get_draft_object() if hasattr(page, 'get_draft_object') else page
    title = draft.get_title(language) or str(draft)
    placeholder = draft.placeholders.get(slot='content')
    blocks = collect_placeholder_plugins(placeholder, language)
    slug = ''
    try:
        slug = draft.get_slug(language) or ''
    except Exception:
        slug = getattr(draft, 'slug', '') or ''

    page_url = ''
    try:
        public = draft.publisher_public or draft
        page_url = public.get_absolute_url() or ''
    except Exception:
        pass

    return PageDocument(
        title=title,
        blocks=blocks,
        slug=slug,
        page_url=page_url,
    )
