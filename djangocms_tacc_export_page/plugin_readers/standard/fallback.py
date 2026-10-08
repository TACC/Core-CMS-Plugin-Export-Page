"""Unknown plugins: children first, then a plain-text line if the model exposes text."""

from __future__ import annotations

from djangocms_tacc_export_page.collector import CollectorContext
from djangocms_tacc_export_page.document import Block
from djangocms_tacc_export_page.html_blocks import collapse_whitespace, html_to_blocks


def read_fallback_plugin(plugin, instance, context: CollectorContext) -> None:
    context.read_children(plugin)
    for attr in ('body', 'name', 'label', 'title'):
        value = getattr(instance, attr, None)
        if not value or not str(value).strip():
            continue
        text = str(value)
        if '<' in text and '>' in text:
            context.extend(html_to_blocks(text))
        else:
            context.extend([Block('paragraph', collapse_whitespace(text))])
        break
