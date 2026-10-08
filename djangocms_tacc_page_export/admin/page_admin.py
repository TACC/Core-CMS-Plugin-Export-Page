"""django CMS page tree: Download as DOCX."""

from __future__ import annotations

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import re_path
from django.utils.html import format_html
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from cms.admin.pageadmin import PageAdmin
from djangocms_tacc_page_export.admin.confirm import nested_page_list
from djangocms_tacc_page_export.export import export_pages_download
from djangocms_tacc_page_export.page_scope import (
    descendant_draft_pages,
    page_qualifies_for_export,
    pages_for_export,
)


class PageExportAdminMixin:
    """Mixin for ``PageAdmin`` — add export URL, confirm view, and actions menu entry."""

    actions_menu_template = 'djangocms_tacc_page_export/admin/page_tree/actions_dropdown.html'

    def get_urls(self):
        info = f'{self.model._meta.app_label}_{self.model._meta.model_name}'
        export_url = re_path(
            r'^([0-9]+)/export-docx/$',
            self.admin_site.admin_view(self.export_docx),
            name=f'{info}_export_docx',
        )
        return [export_url] + super().get_urls()

    def actions_menu(self, request, object_id, extra_context=None):
        page = self.get_object(request, object_id=object_id)
        extra = {
            'page_export_show': bool(
                page
                and self.has_change_permission(request, obj=page)
                and page_qualifies_for_export(page)
            ),
            'page_export_has_children': bool(
                page and descendant_draft_pages(page)
            ),
        }
        extra.update(extra_context or {})
        return super().actions_menu(request, object_id, extra_context=extra)

    def _export_page(self, request, object_id):
        page = self.get_object(request, object_id=object_id)
        if page is None:
            raise self._get_404_exception(object_id)
        if not self.has_change_permission(request, obj=page):
            raise PermissionDenied
        if not page_qualifies_for_export(page):
            raise self._get_404_exception(object_id)
        return page

    def export_docx(self, request, object_id):
        page = self._export_page(request, object_id)
        children_default = request.GET.get('children') == '1'
        descendants = descendant_draft_pages(page)
        scope = (
            f'{page} and its {len(descendants)} child pages'
            if children_default and descendants
            else str(page)
        )
        if request.method != 'POST':
            return render(
                request,
                'djangocms_tacc_page_export/admin/export_confirm.html',
                {
                    **self.admin_site.each_context(request),
                    'opts': self.opts,
                    'title': _('Download as DOCX'),
                    'message': _(
                        'Export draft content from %(scope)s to a Word document?'
                    ) % {'scope': scope},
                    'page': page,
                    'changed_pages': nested_page_list(
                        self,
                        request,
                        pages_for_export(page, children_default),
                    ),
                    'progress_message': _('Building document…'),
                    'include_children_option': bool(descendants),
                    'include_children_default': children_default,
                },
            )
        include_children = request.POST.get('include_children') == '1'
        try:
            filename, content_type, payload = export_pages_download(
                pages_for_export(page, include_children),
            )
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect(self.get_admin_url('changelist'))
        response = FileResponse(
            iter([payload]),
            content_type=content_type,
            as_attachment=True,
            filename=filename,
        )
        response['Content-Length'] = len(payload)
        return response


class PageExportPageAdmin(PageExportAdminMixin, PageAdmin):
    pass
