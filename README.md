## Texas Advanced Computing Center
# Django CMS App (for TACC/Core-CMS): "Page Export"

This app exports **rendered draft** CMS page content (placeholder plugin tree) to **DOCX**, with optional Google Drive export planned for a later phase.

- __Distribution Name__: `djangocms-tacc-page-export`
- __Package Name__: `djangocms_tacc_page_export`
- __Class Name__: `TaccsitePageExport`
- __App Name__: "Page Export"

See [docs/plan-core-cms-page-export.md](docs/plan-core-cms-page-export.md) for product scope, code layout, and delivery steps.

## Quick Start

1. Install the package:

    ```bash
    pip install djangocms-tacc-page-export
    ```

    For local development from a clone:

    ```bash
    pip install -e .
    ```

2. Add to `INSTALLED_APPS` in your Django project settings:

    ```python
    INSTALLED_APPS = [
        ...
        'djangocms_tacc_page_export',
        ...
    ]
    ```

3. Run migrations when the app defines models:

    ```bash
    python manage.py migrate djangocms_tacc_page_export
    ```

For a site using **TACC/Core-CMS** or **Core-CMS-Port**, follow [Core-CMS Getting Started](https://github.com/TACC/Core-CMS#getting-started) and install this package into the CMS environment (same pattern as [Core-CMS-Plugin-Remote-Content](https://github.com/TACC/Core-CMS-Plugin-Remote-Content)).

## Usage

Phase 1 (in progress): **Download as DOCX** from Generated / port page admin actions in Core-CMS-Port. Until integration ships, this package is a scaffold only.

## Features

- Planned DOCX export from CMS plugin trees (standard django CMS plugins plus optional TACC readers when Core-CMS apps are present).
- Planned multi-page export (zip of per-slug `.docx` files).
- Google Drive save (user OAuth) deferred to Phase 2 — see the plan doc.

## Testing

Follow [TESTING.md](TESTING.md).
