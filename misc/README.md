# Miscellaneous

Development-support files. **None of this is released** — `build_ignore` in
`galaxy.yml` keeps the whole directory out of the collection tarball, and it
exists only to support work on the collection.

Four kinds of thing live here, with very different lifetimes. Read this table
before adding anything, so the next file lands in the right category.

| What | Files | Tracked in git? | Lifetime |
|---|---|---|---|
| Host-fact reference dumps | [`facts/`](facts/) — `*.setup`, `*.package_facts`, `*.service_facts` | yes | indefinite |
| Extracted Checkmk API specs | [`openapi/`](openapi/) | **no** | regenerate per Checkmk version |
| Working reports | [`notes/`](notes/) — the files listed below | **no** | until the work they describe lands |
| Audit workspace | [`audit/`](audit/) | **no** | until the findings are closed |

## Host-fact reference dumps

In [`facts/`](facts/). Output of `ansible -m setup` (`.setup`), `ansible -m package_facts`
(`.package_facts`) and `ansible -m service_facts` (`.service_facts`), captured
per distribution. Kept as a reference for looking up the exact value and shape of
a fact without booting a VM — the roles branch on several of these.

## Extracted Checkmk API specs

Everything the extraction produces lives in [`openapi/`](openapi/), which
[`scripts/openapi.sh`](../scripts/openapi.sh) writes to by default (creating it if
needed) and `-o DIR` overrides.

`openapi/openapi-doc-<version>.yaml` and `openapi/openapi-swagger-ui-<version>.yaml`
are the **served** REST API specification
(`/check_mk/api/1.0/openapi-{doc,swagger-ui}.yaml`), pulled from a running site.
Each pair has an `openapi/openapi-<version>.provenance` recording the exact build
the dump came from — always keep them together, because a spec without its build
string cannot be reasoned about. That lesson is written up in
`otel_rest_missing.md`, where an earlier pair of undated dumps supported a
conclusion the provenance later contradicted.

These are large (2–2.8 MB each, ~19 MB total) and regenerable. Note the served
spec is **not** the internal one (`/api/internal`) that the OpenTelemetry modules
call; that one needs bazel and a source checkout, and no dump of it currently
exists on disk.
