# Plan: TACC Core-CMS Page Export

Standalone Django app (future repo **TACC/Core-CMS-Page-Export**). Lives **outside** Core-CMS and Core-CMS-Port forever; Core-CMS and port images **install** it like other TACC plugins. Aligns with TACC practice: optional packages, not everything bundled in Core-CMS (full split not achieved yet).

**django-cms:** 3.11+ and &lt; 4 (current Core-CMS image).

---

## Product

Export **rendered draft** content from Generated / CMS pages (placeholder plugin tree), not scraped HTML.

| Phase | Feature | Google |
|-------|---------|--------|
| **1** | **Download `.docx`** (page + optional children) | None |
| **2** | **Save to Google Drive** (user OAuth, narrow scopes) | See [Phase 2](#phase-2-save-to-google-drive) |

---

## Repository and packaging

- **New repo:** `TACC/Core-CMS-Page-Export` (name TBD).
- **Django app** inside repo (e.g. `djangocms_page_export` or `taccsite_page_export`).
- **Dependencies:** `python-docx`; Google libraries only when Phase 2 is implemented.
- **Consumers:** Core-CMS-Port (`cms_port` page actions), later Core-CMS template/Camino via `INSTALLED_APPS` + settings.
- **Port repo:** keep a copy of this plan under `docs/` until the new repo exists; then link from port docs to the canonical README in the export repo.

---

## Code layout (plugin readers)

Export **must** be split in code, not only in docs:

```
plugin-readers/
  standard/     # django CMS + djangocms-bootstrap4 (etc.) — always available
  tacc/         # Taccsite Card, Section, Link, … — registered only if Core-CMS apps present
registry.py     # dispatches by plugin model; setting to disable TACC layer
```

- TACC `plugin-readers/tacc/` register when their Django apps are installed (`apps.is_installed`); omit Taccsite apps → no TACC readers.
- Optional opt-out: `CMS_PAGE_EXPORT_SHOULD_READ_TACCSITE_PLUGINS = False` (standard readers only).
- Unknown plugins: skip or plain-text fallback (documented per release).

---

## UX (Phase 1)

Mirror existing **cms_port** page-tree actions (`PortPageAdmin`, confirm view):

- **Download as DOCX** — current Generated page; checkbox **Include child pages**.
- Output: single `.docx` or `.zip` of `{slug}.docx` when multiple pages.
- Actions only when `port_page(page)` is set (same rules as refresh/clear/scrape).

Implementation can start in **Core-CMS-Port** calling into the export package once the app exists; or bootstrap the app inside port and extract repo early.

---

## Phase 1 delivery steps

1. **Spike** — 1–2 NAIRR Generated pages; map plugins → document blocks → DOCX.
2. **Scaffold repo** — app, `pyproject.toml`/install, minimal README, CI lint.
3. **Document model** — headings, paragraphs, lists, links; extend for TACC plugins.
4. **DOCX writer** — `python-docx`.
5. **Integration** — port `cms_port` admin route + confirm; wire `page_actions` descendant list.
6. **Docs** — install for Camino/Core-CMS-Port; plugin support matrix.

---

## Phase 2: Save to Google Drive

**Deferred.** Track as a **GitHub issue** in the new export repo when it exists (do not block Phase 1).

### Model

- **User OAuth** (editor signs in with **their** Google account). Not a TACC service account.
- **OAuth client** (Google Console naming: “app”): TACC-owned by default; client may override with their own client ID/secret in `settings_custom`.
- **Terminology in our docs/code:** **client**; say “Google OAuth app” only when referring to Google’s UI.

### Credentials (TACC client)

- **One Client ID + one client secret** shared across all CMS hosts using TACC’s client.
- Register each environment **redirect URI** (admin callback after login — **different hostname** per dev/pprd/prod).
- **Recommended:** second OAuth client (second ID/secret) for **dev/pprd/local** vs **prod** so a leak only rotates non-prod.

### Scopes (least privilege)

- `https://www.googleapis.com/auth/drive.file` — files this app creates/opens, not whole Drive.
- `https://www.googleapis.com/auth/documents` — edit Docs content for those files.
- Avoid full `…/auth/drive`.

### Per user

- **Refresh token** stored per Django user after first consent (design: encrypted DB vs session-only — decide in Phase 2 issue).

### Fidelity

- DOCX upload to Drive is adequate for **editorial markup**, not layout parity with the live site (columns, cards, CMS skins simplify).

### Phase 2 issue checklist (for new repo)

- OAuth start/callback views; token storage; `GoogleExporter` sharing block model with DOCX.
- Settings: `CMS_PAGE_EXPORT_GOOGLE_CLIENT_ID`, secret via secrets store, redirect URI.
- Admin action **Save to Google Drive** + success message with doc URL.
- Security review; scope verification on consent screen.

---

## Relation to Core-CMS-Port today

| Item | Action |
|------|--------|
| `export_editor_docs` (scrape → Google API, PR #44) | Deprioritize vs this plan; scrape export is not the long-term product path. |
| `djangocms-export-page` (Maykin, CMS 4+) | Reference only; not a dependency. |
| This plan file in port | Planning artifact until export repo README is canonical. |

---

## Success criteria

- Phase 1: editor downloads DOCX from Generated page tree with no Google setup.
- Package installable without TACC plugins; TACC plugin readers enhance output when present.
- Phase 2 documented and ticketed, not shipped in Phase 1.
