"""Settings helpers for page export."""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

from django.conf import settings

Qualifier = Union[None, str, Callable[[object], bool]]


def should_read_taccsite_plugins() -> bool:
    return getattr(settings, 'CMS_PAGE_EXPORT_SHOULD_READ_TACCSITE_PLUGINS', True)


def page_export_qualifier() -> Qualifier:
    """Optional callable (or dotted path) — export menu only when it returns true."""
    return getattr(settings, 'CMS_PAGE_EXPORT_PAGE_QUALIFIER', None)
