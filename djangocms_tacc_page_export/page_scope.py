"""Which CMS pages are in scope for an export action."""

from __future__ import annotations

from django.utils.module_loading import import_string

from cms.models import Page

from djangocms_tacc_page_export.conf import page_export_qualifier


def page_qualifies_for_export(page) -> bool:
    qualifier = page_export_qualifier()
    if qualifier is None:
        return True
    if callable(qualifier):
        return bool(qualifier(page))
    return bool(import_string(qualifier)(page))


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
