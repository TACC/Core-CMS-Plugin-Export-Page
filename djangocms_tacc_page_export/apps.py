from django.apps import AppConfig


class TaccsitePageExportConfig(AppConfig):
    name = 'djangocms_tacc_page_export'
    verbose_name = 'Page Export'

    def ready(self):
        from django.apps import apps

        from djangocms_tacc_page_export.plugin_readers import register_all_readers

        register_all_readers()
        if apps.is_installed('cms'):
            from djangocms_tacc_page_export.admin import apply_page_export_admin

            apply_page_export_admin()
