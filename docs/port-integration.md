# Core-CMS-Port integration (later)

1. Install the same package and add `djangocms_tacc_page_export` to `INSTALLED_APPS` (via Core-CMS image or Port overlay).
2. In `settings_custom`, limit the menu to Generated pages:

   ```python
   CMS_PAGE_EXPORT_PAGE_QUALIFIER = 'apps.cms_port.common.page_actions.port_page'
   ```

   (`port_page` returns a `PortPage` or `None`; the qualifier treats any truthy value as eligible.)

3. Subclass **both** mixins — export must not replace `PageAdmin` after Port registers:

   ```python
   from djangocms_tacc_page_export.admin.page_admin import PageExportAdminMixin

   class PortPageAdmin(PageExportAdminMixin, PageAdmin):
       actions_menu_template = 'cms_port/page_tree/actions_dropdown.html'
       ...
   ```

4. Extend the export actions template so port items appear after core + export:

   ```django
   {% extends "djangocms_tacc_page_export/admin/page_tree/actions_dropdown.html" %}
   {% block actions %}
       {{ block.super }}
       … port-only items …
   {% endblock %}
   ```

5. Child-page scope on Port may still use the port registry (`target_pages`) instead of the CMS tree; override `export_docx` or add a setting only if product requires that difference.
