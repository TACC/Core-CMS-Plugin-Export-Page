"""TACC Site Section plugin."""

from __future__ import annotations

from djangocms_tacc_page_export.collector import CollectorContext
from djangocms_tacc_page_export.document import Block
from djangocms_tacc_page_export.html_blocks import collapse_whitespace


def read_section_plugin(plugin, instance, context: CollectorContext) -> None:
    label = collapse_whitespace(getattr(instance, 'label', '') or '')
    if label:
        context.extend([Block('heading2', label)])
    context.read_children(plugin)
