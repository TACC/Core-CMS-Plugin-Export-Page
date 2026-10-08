"""djangocms-snippet — plain text fallback from snippet HTML."""

from __future__ import annotations

from djangocms_tacc_page_export.collector import CollectorContext
from djangocms_tacc_page_export.html_blocks import html_to_blocks


def read_snippet_plugin(plugin, instance, context: CollectorContext) -> None:
    snippet = getattr(instance, 'snippet', None)
    html = getattr(snippet, 'html', '') if snippet else ''
    context.extend(html_to_blocks(html))
    context.read_children(plugin)
