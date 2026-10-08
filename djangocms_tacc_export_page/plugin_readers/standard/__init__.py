"""Standard django CMS / bootstrap4 plugin readers."""

from __future__ import annotations

from django.apps import apps as django_apps

from djangocms_tacc_export_page.plugin_readers.registry import register_fallback, register_reader
from djangocms_tacc_export_page.plugin_readers.standard.fallback import read_fallback_plugin
from djangocms_tacc_export_page.plugin_readers.standard.layout import read_children_only
from djangocms_tacc_export_page.plugin_readers.standard.link import read_link_plugin
from djangocms_tacc_export_page.plugin_readers.standard.snippet import read_snippet_plugin
from djangocms_tacc_export_page.plugin_readers.standard.text import read_text_plugin

_LAYOUT_PLUGIN_TYPES = (
    'Bootstrap4GridContainerPlugin',
    'Bootstrap4GridRowPlugin',
    'Bootstrap4GridColumnPlugin',
    'StylePlugin',
    'Bootstrap4AlertsPlugin',
)


def register_standard_readers() -> None:
    register_reader('TextPlugin', read_text_plugin)
    register_reader('Bootstrap4LinkPlugin', read_link_plugin)
    if django_apps.is_installed('djangocms_snippet'):
        register_reader('SnippetPlugin', read_snippet_plugin)
    for plugin_type in _LAYOUT_PLUGIN_TYPES:
        register_reader(plugin_type, read_children_only)
    register_fallback(read_fallback_plugin)
