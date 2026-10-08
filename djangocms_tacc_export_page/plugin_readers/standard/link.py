"""Bootstrap4 Link / Button plugin."""

from __future__ import annotations

from djangocms_tacc_export_page.collector import CollectorContext
from djangocms_tacc_export_page.document import Block


def _link_url(instance) -> str:
    if getattr(instance, 'external_link', None):
        return instance.external_link or ''
    page = getattr(instance, 'page_link', None)
    if page:
        try:
            return page.get_absolute_url() or ''
        except Exception:
            return ''
    file = getattr(instance, 'file_link', None)
    if file:
        try:
            return file.url or ''
        except Exception:
            return ''
    return ''


def read_link_plugin(plugin, instance, context: CollectorContext) -> None:
    name = (getattr(instance, 'name', None) or '').strip()
    url = _link_url(instance).strip()
    if name or url:
        context.extend([Block('link_line', name or url, url=url or None)])
    context.read_children(plugin)
