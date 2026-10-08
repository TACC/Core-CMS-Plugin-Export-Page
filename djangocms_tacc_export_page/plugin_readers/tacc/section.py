"""TACC Site Section plugin — structure label is editor-only, not on the public page."""

from __future__ import annotations

from djangocms_tacc_export_page.collector import CollectorContext


def read_section_plugin(plugin, instance, context: CollectorContext) -> None:
    context.read_children(plugin)
