"""Which CMS pages are included in an export (scope / descendants)."""

from __future__ import annotations

from cms.models import Page


def draft_page(page) -> Page:
    return page.get_draft_object() if hasattr(page, 'get_draft_object') else page


def descendant_draft_pages(page) -> list[Page]:
    root = draft_page(page)
    nodes = root.node.get_descendants()
    if not nodes.exists():
        return []
    return list(
        Page.objects.drafts()
        .filter(node__in=nodes)
        .order_by('node__path')
    )


def pages_for_export(page, include_children: bool) -> list[Page]:
    root = draft_page(page)
    if not include_children:
        return [root]
    return [root] + descendant_draft_pages(page)
