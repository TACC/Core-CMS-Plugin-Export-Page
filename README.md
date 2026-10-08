## Texas Advanced Computing Center
# Django CMS App: "Page Export"

This app exports **rendered draft** CMS page content (placeholder plugin tree) to **DOCX**, with optional Google Drive export planned for a later phase.

- __`__dist-name__`__: `djangocms-tacc-page-export`
- __`__package_name__`__: `djangocms_tacc_page_export`
- __`__ClassName__`__: `TaccsitePageExport`
- __"App Name"__: "Page Export"

See [docs/plan-core-cms-page-export.md](docs/plan-core-cms-page-export.md) for Phase 2 (Google Drive) and long-term scope.

## Quick Start

1. Follow [(wiki) Usage Quick Start](https://github.com/TACC/Django-App/wiki/Usage-Quick-Start).

## Usage

Phase 1: **Download as DOCX** from the CMS page tree when this app is in `INSTALLED_APPS` (wired in [Core-CMS](https://github.com/TACC/Core-CMS)). See [docs/plugin-support.md](docs/plugin-support.md). [Core-CMS-Port](https://github.com/TACC/Core-CMS-Port) integration is documented in [docs/port-integration.md](docs/port-integration.md).

TACC/Core-CMS plugin readers in `plugin-readers/tacc/` register automatically when the corresponding apps are in `INSTALLED_APPS` (same idea as `apps.is_installed()` elsewhere in Core-CMS). To export with standard django CMS readers only, even when Taccsite apps are installed:

```python
CMS_PAGE_EXPORT_SHOULD_READ_TACCSITE_PLUGINS = False
```

## Permissions

Only **superusers** and **staff users who can edit a page** can export that page’s draft content (toolbar **Download**, page-tree **Download…**, and the export URL all use django CMS **change page** permission). Staff without edit access on a page do not see the actions and cannot download via the admin URL.

## Features

- DOCX export from CMS plugin trees (standard django CMS plugins plus optional TACC readers when Core-CMS apps are present).
- Multi-page export (zip of per-slug `.docx` files).
- Google Drive save (user OAuth) in Phase 2 — see the plan doc.

## Testing

Follow [TESTING.md](TESTING.md).
