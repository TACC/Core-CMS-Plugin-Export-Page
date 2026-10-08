"""djangocms-text-ckeditor Text plugin."""

from __future__ import annotations

from djangocms_tacc_page_export.collector import CollectorContext
from djangocms_tacc_page_export.html_blocks import html_to_blocks


def read_text_plugin(plugin, instance, context: CollectorContext) -> None:
    body = getattr(instance, 'body', '') or ''
    context.extend(html_to_blocks(body))
    context.read_children(plugin)
