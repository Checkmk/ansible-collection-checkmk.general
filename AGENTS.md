# AGENTS.md

> **Preface:** This repository uses AI agents for development, triage, debugging,
> and — alongside a human — code review. A human maintainer reviews and approves
> every change before it lands; agents augment, they do not replace.

## Project Overview

Official Checkmk Ansible Collection (`checkmk.general`): modules,
lookup/inventory plugins, and roles for deploying and managing Checkmk
monitoring sites and monitored hosts.

## Setup

```bash
uv venv && uv sync   # tooling pinned in pyproject.toml / uv.lock
```

Published-collection install (consumers, not development): see [`INSTALL.md`](INSTALL.md).

## Build & Test

All tooling runs via `uv run`. `ansible-test` requires `--docker` **last**, after any target paths.

```bash
uv run ansible-test sanity --docker
uv run ansible-test units --docker
uv run ansible-test units tests/unit/plugins/<path> --docker   # single target
uv run ansible-test integration --docker
cd roles/server && uv run molecule test -s 2.5    # scenarios: 2.3 / 2.4 / 2.5 (default/ is a symlink to 2.5)
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the human-oriented guide.

## Code Style

- Python: `black` + `isort` (profile=`black`).
- YAML / Ansible: `yamllint` + `ansible-lint` (configs: [`.yamllint`](.yamllint), [`.ansible-lint`](.ansible-lint)).
- Module options: simple (`name`) for single-class modules, qualified (`host_name`) for multi-class. Aliases only for deprecation.
- Role/playbook vars: `snake_case`, prefixed `checkmk_{server,agent,var}_*`. Internal: `__`. Tags use dashes.

## Project Structure

```
plugins/
  modules/         modules wrapping the Checkmk REST API
  inventory/       dynamic inventory plugin
  lookup/          lookup plugins
  module_utils/    api.py (REST), differ.py, utils.py, discovery_<ver>.py
  doc_fragments/   reusable DOCUMENTATION blocks
roles/
  {agent,server}/  install/manage Checkmk agent / server site
tests/
  unit/plugins/    pytest unit tests, mirrors plugins/ layout
  integration/     one target per module/lookup (lookup_* prefix for lookups)
changelogs/
  fragments/       per-PR changelog fragments (.yml) — required
docs/              generated module docs — do NOT hand-edit
```

Modules and tests are name-aligned: `plugins/modules/host.py` ↔ `tests/integration/targets/host/` ↔ `tests/unit/plugins/modules/test_host.py`.

## Conventions

- Module docs live inline (`DOCUMENTATION` / `EXAMPLES` / `RETURN`); `docs/` is generated.
- Per-version discovery branching lives in `plugins/module_utils/discovery_<ver>.py`.

## Do & Don't

- **Do** copy an existing module / lookup / integration target when adding a new one.
- **Do** run `uv run ansible-test sanity --docker` after making changes.
- **Don't** reimplement HTTP / REST plumbing — reuse [`plugins/module_utils/api.py`](plugins/module_utils/api.py).
- **Don't** use `site` as a top-level module option; it collides with `base_argument_spec()` — remap to e.g. `target_site`.

## Adding a new module / lookup plugin

Touch every item below:

- `meta/runtime.yml` — add module name to `action_groups.checkmk` (modules only, not lookups).
- `.github/labels-issues.yml` — `module:<name>` or `lookup:<name>` block, with `Component Name:` entries (singular and plural for paired lookups).
- `.github/labels-prs.yml` — same key, with `changed-files` glob. Lookup glob is `plugins/lookup/<name>{,s}.py` — pre-existing `lookup:*` entries point at the non-existent `plugins/modules/lookup/`; don't copy that.
- `.github/workflows/ans-int-test-<name>.yaml` (modules) or `ans-int-test-lkp-<name>.yaml` (lookups); for modules also `ans-unit-test-<name>.yaml` if you add unit tests.
- `README.md` — row in the Modules or Lookup plugins table with CI badge.
- `changelogs/fragments/<name>.yml` — one entry per plugin (module + each lookup).
- `tests/integration/targets/<name>/` (modules) or `tests/integration/targets/lookup_<name>/` (lookups); for modules also `tests/unit/plugins/modules/test_<name>.py` if applicable.
- `docs/` is generated — skip.

## Pull Requests

- **Target:** `devel`, never `main`.
- **Commits:** present tense, imperative, ≤72 char title.
- **Changelog fragment (mandatory):** `.yml` in `changelogs/fragments/`, copy [`template.yml`](changelogs/template.yml). Format:

  ```yaml
  bugfixes:
    - host module - Fix crash when ``attributes`` is empty.
  ```

  Scope = module/plugin name or group; description starts uppercase, ends with a period. Plugin names take the type suffix (`foo inventory plugin`); modules stand alone. Keys: `breaking_changes`, `major_changes`, `minor_changes`, `bugfixes`, `deprecated_features`, `removed_features`, `security_fixes`, `known_issues`, `release_summary`.
- **CI:** sanity / unit / integration / molecule run on PR creation.
- **CLA:** [signature required](https://github.com/Checkmk/checkmk/blob/master/doc/cla/cla_readme.md) before merge.
- **Review:** every PR approved by a human (see preface).
