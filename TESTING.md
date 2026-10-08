# How to Test on [Core CMS]

[Core CMS]: https://github.com/TACC/Core-CMS

## Automated Testing

1. Install this package into a project e.g. [Core CMS] or [Core-CMS-Port](https://github.com/TACC/Core-CMS-Port).
2. When tests exist, run:

    ```sh
    docker exec core_cms python manage.py test djangocms_tacc_page_export
    ```

## Manual Testing

Manual export flows will be documented when Phase 1 admin integration lands in Core-CMS-Port. Until then, verify the package installs and the app loads:

1. Follow [TACC/Core-CMS "Getting Started"](https://github.com/TACC/Core-CMS#getting-started) (use a **git worktree** if another checkout already owns `main`).
2. Add `djangocms_tacc_page_export` to `INSTALLED_APPS` and install this repo (`pip install -e /path/to/Core-CMS-Plugin-Page-Export`).
3. Run `python manage.py check` with no errors.
