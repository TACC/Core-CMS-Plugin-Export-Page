# Core-CMS-Port integration (later)

1. Install the same package and add `djangocms_tacc_page_export` to `INSTALLED_APPS` (via Core-CMS image or Port overlay).

2. Subclass **both** mixins — export must not replace `PageAdmin` after Port registers:

   ```python
   from djangocms_tacc_page_export.admin.page_admin import PageExportAdminMixin

   class PortPageAdmin(PageExportAdminMixin, PageAdmin):
       actions_menu_template = 'cms_port/page_tree/actions_dropdown.html'
       ...
   ```

   To limit export to port/generated pages only, override `actions_menu` (set `page_export_show`) or `export_docx` in `PortPageAdmin` using existing `port_page()` helpers — same pattern as scrape/refresh visibility.

3. Extend the export actions template so port items appear after core + export:

   ```django
   {% extends "djangocms_tacc_page_export/admin/page_tree/actions_dropdown.html" %}
   {% block actions %}
       {{ block.super }}
       … port-only items …
   {% endblock %}
   ```

4. Child-page scope on Port may still use the port registry (`target_pages`) instead of the CMS tree; override `export_docx` only if product requires that difference.
