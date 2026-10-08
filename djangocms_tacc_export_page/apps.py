from django.apps import AppConfig


class TaccsiteExportPageConfig(AppConfig):
    name = 'djangocms_tacc_export_page'
    verbose_name = 'Export Page'

    def ready(self):
        from django.apps import apps

        from djangocms_tacc_export_page.plugin_readers import register_all_readers

        register_all_readers()
        if apps.is_installed('cms'):
            from djangocms_tacc_export_page.admin import apply_export_page_admin

            apply_export_page_admin()
            # Register toolbar (import side effect).
            from djangocms_tacc_export_page import cms_toolbar  # noqa: F401
