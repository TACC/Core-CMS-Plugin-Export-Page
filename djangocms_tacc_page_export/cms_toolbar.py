"""CMS toolbar: right-side Export button (while editing a page)."""

from __future__ import annotations

from cms.api import get_page_draft
from cms.constants import RIGHT
from cms.toolbar.items import TemplateItem
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.page_permissions import user_can_change_page
from cms.utils.urlutils import admin_reverse

def export_docx_url_for_page(page) -> str:
    return admin_reverse('cms_page_export_docx', args=[page.pk])


@toolbar_pool.register
class PageExportToolbar(CMSToolbar):
    """Add **Download** on the toolbar right (next to Create / View published)."""

    def post_template_populate(self):
        current = self.request.current_page
        if not current:
            return
        page = get_page_draft(current)
        if not user_can_change_page(self.request.user, page=page, site=self.current_site):
            return

        item = TemplateItem(
            template='djangocms_tacc_page_export/cms_toolbar/export_button.html',
            extra_context={'export_url': export_docx_url_for_page(page)},
            side=RIGHT,
        )
        self.toolbar.add_item(item)
