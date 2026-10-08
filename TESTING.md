# How to Test on [Core CMS]

[Core CMS]: https://github.com/TACC/Core-CMS

## Automated Testing

1. Install this package into a project e.g. [Core CMS] or [Core-CMS-Port](https://github.com/TACC/Core-CMS-Port).
2. When tests exist, run:

    ```sh
    docker exec core_cms python manage.py test djangocms_tacc_page_export
    ```

## Manual Testing

1. In [Core-CMS](https://github.com/TACC/Core-CMS), ensure `djangocms-tacc-page-export` is installed (Poetry path to this repo) and rebuild (`make build`).
2. Page tree → any page → **Download as DOCX…** (optional **Include child pages**).
3. Open the `.docx` or `.zip` and confirm content matches the draft **content** placeholder.
