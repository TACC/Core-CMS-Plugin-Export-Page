"""Bootstrap grid and Style plugins — export child content only."""

from __future__ import annotations

from djangocms_tacc_export_page.collector import CollectorContext


def read_children_only(plugin, instance, context: CollectorContext) -> None:
    context.read_children(plugin)
