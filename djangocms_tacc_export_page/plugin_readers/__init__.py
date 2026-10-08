"""Plugin reader registry bootstrap."""

from __future__ import annotations

from djangocms_tacc_export_page.plugin_readers.standard import register_standard_readers
from djangocms_tacc_export_page.plugin_readers.tacc import register_taccsite_readers


def register_all_readers() -> None:
    register_standard_readers()
    register_taccsite_readers()
