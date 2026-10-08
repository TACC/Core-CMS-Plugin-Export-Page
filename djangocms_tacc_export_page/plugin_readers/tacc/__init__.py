"""TACC Site plugin readers (registered when Taccsite apps are installed)."""

from __future__ import annotations

from django.apps import apps as django_apps

from djangocms_tacc_export_page.plugin_readers.registry import register_reader
from djangocms_tacc_export_page.plugin_readers.tacc.card import read_card_plugin
from djangocms_tacc_export_page.plugin_readers.tacc.section import read_section_plugin


def register_taccsite_readers() -> None:
    if django_apps.is_installed('taccsite_section'):
        register_reader('TaccsiteSectionPlugin', read_section_plugin)
    if django_apps.is_installed('taccsite_card'):
        register_reader('TaccsiteCardPlugin', read_card_plugin)
