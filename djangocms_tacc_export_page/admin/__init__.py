"""Register page-tree export on django CMS ``PageAdmin`` when appropriate."""

from __future__ import annotations


def _admin_class_has_export_mixin(admin_class: type) -> bool:
    from djangocms_tacc_export_page.admin.page_admin import ExportPageAdminMixin

    return issubclass(admin_class, ExportPageAdminMixin)


def apply_export_page_admin() -> None:
    from cms.admin.pageadmin import PageAdmin
    from cms.models import Page
    from django.contrib import admin

    from djangocms_tacc_export_page.admin.page_admin import (
        ExportPageAdminMixin,
        ExportPageAdmin,
    )

    if not admin.site.is_registered(Page):
        return
    current_class = admin.site._registry[Page].__class__
    if _admin_class_has_export_mixin(current_class):
        return
    if current_class is not PageAdmin:
        return
    admin.site.unregister(Page)
    admin.site.register(Page, ExportPageAdmin)
