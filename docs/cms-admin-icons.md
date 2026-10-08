# django CMS admin icon font (`cms-icon-*`)

Page export uses **text only** (toolbar **Export**, tree **Download as DOCX…**) — there is no suitable download glyph in this font.

## Preview glyphs (visual)

django CMS does not ship a public icon gallery page. Practical options:

1. **In your CMS (best context)** — **Pages** (`/admin/cms/page/`) → row **⋯** menu: Copy (`cms-icon-copy`), Cut (`cms-icon-scissors`), Delete (`cms-icon-bin`), etc.
2. **Font file** — Drop the icon font into [FontDrop](https://fontdrop.info/):
   - Match your installed django-cms version (e.g. 3.11.4):  
     [django-cms-iconfont.woff (3.11.4)](https://github.com/django-cms/django-cms/raw/release/3.11.x/cms/static/cms/fonts/3.11.4/django-cms-iconfont.woff)
   - Or use the version path from your container:  
     `python -c "import cms, os; print(os.path.dirname(cms.__file__))"` → `static/cms/fonts/<version>/`
3. **SVG font** (some browsers show glyphs in the XML):  
   [django-cms-iconfont.svg (3.11.4)](https://github.com/django-cms/django-cms/raw/release/3.11.x/cms/static/cms/fonts/3.11.4/django-cms-iconfont.svg)

## Class list (names only)

Authoritative source for your django-cms release branch:

- [_iconography.scss (release/3.11.x)](https://github.com/django-cms/django-cms/blob/release/3.11.x/cms/static/cms/sass/components/_iconography.scss)

| Class | Typical use in CMS |
| --- | --- |
| `cms-icon-alias` | Paste |
| `cms-icon-arrow` | Menu / sideframe chevron |
| `cms-icon-arrow-right` | Forward |
| `cms-icon-arrow-wide` | Wide arrow |
| `cms-icon-bin` | Delete |
| `cms-icon-check` / `cms-icon-check-o` / `cms-icon-check-square` | States |
| `cms-icon-close` | Close |
| `cms-icon-cogs` | Advanced settings |
| `cms-icon-copy` | Copy page |
| `cms-icon-eye` | View |
| `cms-icon-forbidden` | Disabled |
| `cms-icon-handler` | Drag handle |
| `cms-icon-highlight` | Plugin highlight |
| `cms-icon-home` | Set home |
| `cms-icon-info` | Info |
| `cms-icon-loader` | Loading |
| `cms-icon-lock` | Permissions |
| `cms-icon-logo` | Brand |
| `cms-icon-menu` | Menu |
| `cms-icon-minimize` / `cms-icon-minus` / `cms-icon-minus-square` / `cms-icon-minus-square-o` | Collapse / remove |
| `cms-icon-paste` | Paste (alt) |
| `cms-icon-pencil` | Edit |
| `cms-icon-pin` | Pin |
| `cms-icon-plugins` | Structure mode toggle |
| `cms-icon-plus` / `cms-icon-plus-square-o` | Add |
| `cms-icon-puzzle` | Plugins |
| `cms-icon-scissors` | Cut |
| `cms-icon-search` | Search |
| `cms-icon-sitemap` | Tree |
| `cms-icon-squares` | Grid |
| `cms-icon-theme-auto` / `cms-icon-theme-dark` / `cms-icon-theme-light` | Toolbar theme |
| `cms-icon-window` | Maximize modal (not export) |

Toolbar **Page** menu items are text-only; icons apply to **page tree ⋯**, toolbar **Structure** control, etc.

**Not** the same set as TACC Cortal `icon-*` classes on public pages.
