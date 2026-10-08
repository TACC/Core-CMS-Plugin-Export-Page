"""TACC Site Card plugin — export nested text like a mini section."""

from __future__ import annotations

from djangocms_tacc_export_page.collector import CollectorContext
from djangocms_tacc_export_page.plugin_readers.standard.layout import read_children_only


def read_card_plugin(plugin, instance, context: CollectorContext) -> None:
    read_children_only(plugin, instance, context)
