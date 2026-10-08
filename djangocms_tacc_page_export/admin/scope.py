"""Helpers for the export scope form (pages with children)."""

from __future__ import annotations

from django.utils.html import format_html
from django.utils.text import capfirst


def nested_page_list(page_admin, request, pages):
    """Nested list like Django's ``deleted_objects``, nested by page tree."""
    opts = page_admin.opts
    roots, stack = [], []
    for page in pages:
        while stack and not page.node.path.startswith(stack[-1][0]):
            stack.pop()
        public_page = page.publisher_public or page
        item = format_html(
            '{}: <a href="{}">{}</a>',
            capfirst(opts.verbose_name),
            public_page.get_absolute_url(),
            page,
        )
        children = []
        (stack[-1][1] if stack else roots).extend([item, children])
        stack.append((page.node.path, children))
    return roots
