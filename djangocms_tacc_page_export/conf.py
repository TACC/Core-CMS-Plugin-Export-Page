"""Settings helpers for page export."""

from __future__ import annotations

from django.conf import settings


def should_read_taccsite_plugins() -> bool:
    return getattr(settings, 'CMS_PAGE_EXPORT_SHOULD_READ_TACCSITE_PLUGINS', True)
