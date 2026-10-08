"""Plugin reader protocol."""

from __future__ import annotations

from typing import Protocol

from djangocms_tacc_page_export.collector import CollectorContext


class PluginReader(Protocol):
    def read(self, plugin, instance, context: CollectorContext) -> None:
        """Append export blocks for ``plugin`` (and optionally descendants)."""
