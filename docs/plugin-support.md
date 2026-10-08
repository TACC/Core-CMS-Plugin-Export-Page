# Plugin support (Phase 1)

Export walks the draft **content** placeholder plugin tree. Layout plugins pass through to children; text becomes headings, paragraphs, and lists.

| Plugin | Reader behavior |
| --- | --- |
| Text | HTML body → blocks |
| Bootstrap4 grid (container / row / column) | Children only |
| Style | Children only |
| Bootstrap4 Link / Button | Link line (`label (url)`) |
| Bootstrap4 Alert | Children only |
| Snippet | Snippet HTML → blocks (when `djangocms_snippet` is installed) |
| TACC Site Section | Section label → heading 2, then children |
| TACC Site Card | Children only |
| Other | Children, then plain `body` / `name` / `label` / `title` if present |

Unknown plugins are skipped after the fallback pass. Set `CMS_PAGE_EXPORT_SHOULD_READ_TACCSITE_PLUGINS = False` to omit TACC Site readers even when those apps are installed.
