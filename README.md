## Texas Advanced Computing Center
# Django CMS App: "Page Export"

This app exports **rendered draft** CMS page content (placeholder plugin tree) to **DOCX**, with optional Google Drive export planned for a later phase.

- __`__dist-name__`__: `djangocms-tacc-page-export`
- __`__package_name__`__: `djangocms_tacc_page_export`
- __`__ClassName__`__: `TaccsitePageExport`
- __"App Name"__: "Page Export"

<!-- Remove plan doc link after export is implemented. -->
See [docs/plan-core-cms-page-export.md](docs/plan-core-cms-page-export.md) for product scope, code layout, and delivery steps.

## Quick Start

1. Follow [(wiki) Usage Quick Start](https://github.com/TACC/Django-App/wiki/Usage-Quick-Start).

## Usage

Phase 1 (in progress): **Download as DOCX** from Generated / port page admin actions in Core-CMS-Port. Until integration ships, this package is a scaffold only.

TACC/Core-CMS plugin readers in `plugin-readers/tacc/` register automatically when the corresponding apps are in `INSTALLED_APPS` (same idea as `apps.is_installed()` elsewhere in Core-CMS). To export with standard django CMS readers only, even when Taccsite apps are installed:

```python
CMS_PAGE_EXPORT_SHOULD_READ_TACCSITE_PLUGINS = False
```

## Features

- **Planned** DOCX export from CMS plugin trees (standard django CMS plugins plus optional TACC readers when Core-CMS apps are present).
- **Planned** multi-page export (zip of per-slug `.docx` files).
- **Planned** Google Drive save (user OAuth) in Phase 2 — see the plan doc.

## Testing

Follow [TESTING.md](TESTING.md).
