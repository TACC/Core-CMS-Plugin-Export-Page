"""CMS toolbar: Page menu → Download as DOCX."""

from __future__ import annotations

from django.utils.translation import gettext_lazy as _

from cms.api import get_page_draft
from cms.cms_toolbars import PAGE_MENU_IDENTIFIER, PAGE_MENU_SECOND_BREAK
from cms.toolbar.items import Break
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.page_permissions import user_can_change_page
from cms.utils.urlutils import admin_reverse

from djangocms_tacc_page_export.page_scope import page_qualifies_for_export


@toolbar_pool.register
class PageExportToolbar(CMSToolbar):
    """Add export link to the built-in **Page** toolbar menu (while editing a page)."""

    def populate(self):
        current = self.request.current_page
        if not current:
            return
        page = get_page_draft(current)
        if not page_qualifies_for_export(page):
            return
        if not user_can_change_page(self.request.user, page=page, site=self.current_site):
            return

        menu = self.toolbar.get_menu(PAGE_MENU_IDENTIFIER)
        if menu is None:
            return

        url = admin_reverse('cms_page_export_docx', args=[page.pk])
        insert_before = menu.find_first(Break, identifier=PAGE_MENU_SECOND_BREAK)
        menu.add_link_item(
            _('Download as DOCX…'),
            url=url,
            position=insert_before,
        )
