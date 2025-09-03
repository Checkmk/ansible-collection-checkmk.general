# Execution Environment guide

An [Execution Environment](https://docs.ansible.com/ansible/latest/getting_started_ee/index.html)
(EE) is a container image that bundles everything needed to *run* Ansible content: a
Python interpreter, `ansible-core`, `ansible-runner`, system libraries, and a set of
collections. Instead of getting the right versions onto a control node by hand, you run
your playbooks inside one image. `ansible-navigator` and Ansible Automation Platform both
execute playbooks this way.

This collection ships a definition for building such an image.

> [!IMPORTANT]
> This is a proof of concept. **No image is published anywhere yet** — there is no
> registry to pull from, and no support commitment. You build it yourself from a checkout
> of this repository. If you only want to *use* the collection, see
> [INSTALL.md](INSTALL.md) instead; you do not need any of this.

## What is in the image

| | |
|---|---|
| Base image | `quay.io/centos/centos:stream10` |
| Python | 3.12 (`/usr/bin/python3`, the base image default) |
| `ansible-core` | 2.20.9 |
| `ansible-runner` | latest |
| System packages | `openssh-clients` |
| Collections | `checkmk.general` **from your working tree**, plus its dependencies: `ansible.posix`, `ansible.windows`, `community.general` |
| Size | roughly 310 MB |

Collections are installed to `/usr/share/ansible/collections/ansible_collections/`.

CentOS Stream 10 was chosen for its long support window. Its default `python3` is 3.12,
which satisfies `ansible-core`'s requirement of Python 3.11 or newer on the control node —
RHEL, CentOS and Rocky 9 ship Python 3.9 and would need an explicit `python3.12` package.

### The image is built from your checkout, not from Galaxy

This matters. The image contains the collection **as it exists in your working tree**, not
the version published on Ansible Galaxy. Build from a release tag and the image matches
that release exactly, with no waiting for Galaxy to propagate. Build from a feature branch
and you get your feature branch. There is no version to pin and no way for the image to
silently drift from the source it was built from.

## Prerequisites

- [Podman](https://podman.io/) (Docker works too, but the tooling defaults to Podman here)
- [uv](https://docs.astral.sh/uv/), which the rest of this repository already uses
- Roughly 2 GB of free disk space for the build

`ansible-builder` and `ansible-navigator` are installed automatically into an isolated
environment by the build; you do not need them on your system.

## Building the image

```bash
make ee
```

That is the whole thing. It takes about three minutes on a cold cache.

The target builds the image **and** runs a smoke-test playbook inside it, so a successful
run means more than "the container built" — it means the collection loads, its
documentation parses for every plugin type, and its modules import and execute in the
image.

Expect output ending in something like:

```
PLAY RECAP *********************************************************************
localhost                  : ok=4    changed=0    unreachable=0    failed=0

nox > Session ee-check-centos-stream-10 was successful in 3 minutes.
```

The result is tagged:

```
localhost/checkmk-general-centos-stream-10:latest
```

Confirm what you got:

```bash
podman run --rm localhost/checkmk-general-centos-stream-10:latest \
    ansible-galaxy collection list
```

## Running playbooks with the image

### With `ansible-navigator`

```bash
ansible-navigator run playbooks/demo/hosts-and-folders.yml \
    --execution-environment true \
    --execution-environment-image localhost/checkmk-general-centos-stream-10:latest \
    --container-engine podman \
    --pull-policy never \
    --mode stdout
```

`--pull-policy never` is not optional for a locally built image. Without it,
`ansible-navigator` tries to pull the tag from a registry, fails to find it, and never
reaches your local copy.

Drop `--mode stdout` for the interactive text UI.

### With Ansible Automation Platform

AAP pulls execution environments from a registry, so a locally built image has to be
pushed somewhere the controller can reach it first:

```bash
podman tag localhost/checkmk-general-centos-stream-10:latest \
    registry.example.com/checkmk-general-ee:8.5.0
podman push registry.example.com/checkmk-general-ee:8.5.0
```

Then add it under **Administration → Execution Environments** in the controller and select
it on the relevant job templates.

## Customizing the build

The definition lives in [`antsibull-nox.toml`](antsibull-nox.toml), under
`[[sessions.ee_check.execution_environments]]`. It is not a raw
`execution-environment.yml`; [antsibull-nox](https://ansible.readthedocs.io/projects/antsibull-nox/)
generates that file, which is what guarantees the image is built from local source.

The options most likely to interest you:

| Option | Purpose |
|---|---|
| `base_image_name` | The base container image |
| `ansible_core_package` | The `ansible-core` version. **The only place a concrete version is pinned for the image.** |
| `ansible_runner_package` | The `ansible-runner` version |
| `system_packages` | Packages installed with `dnf` |
| `python_packages` | Additional packages installed with `pip` |
| `test_playbooks` | Playbooks run inside the built image |

The full option reference is in the
[antsibull-nox configuration documentation](https://ansible.readthedocs.io/projects/antsibull-nox/config-file/).

Note the distinction between the pin here and `requires_ansible` in `meta/runtime.yml`.
The latter is the collection's *compatibility floor* — the oldest `ansible-core` the
collection supports. An image needs exactly one concrete version, which is what
`ansible_core_package` provides. They are different statements and are not expected to
match.

After editing, rebuild with `make ee`.

### Password-based SSH

`sshpass` is deliberately **not** in the image. The collection does not need it, and it is
not in the CentOS base repositories — only in EPEL, which is a dependency this image does
not take on your behalf.

If your inventory authenticates over SSH with a password rather than a key, add EPEL and
the package yourself:

```toml
system_packages = ["openssh-clients", "epel-release", "sshpass"]
```

## Troubleshooting 💡

### `permission denied` creating `.../mnt/rootfs`

```
error running container: creating directory ".../mnt/rootfs": permission denied
```

You ran `nox` directly instead of `make ee`, inside the Vagrant development box. The
collection root is shared into the box over virtiofs, which buildah cannot use for its
container rootfs mounts, and nox places each session's temporary directory inside its
environment directory — which lands on that share.

Setting `TMPDIR` does not help; nox overrides it per session. Use `make ee`, which points
the environment directory at local storage, or pass `--envdir` yourself:

```bash
uv run nox --envdir /tmp/nox-checkmk-general -s ee-check
```

This only affects the development box. It is not an issue on GitHub runners or on a normal
workstation checkout.

### `ansible-navigator` cannot find the image

Pass `--pull-policy never`. See [above](#with-ansible-navigator).

### The image contains the wrong collection version

It contains whatever is in your working tree. Check out the branch or tag you actually
want and rebuild — there is no cache to clear and no version to pin.

## Continuous integration

The [`Execution Environment`](.github/workflows/execution-environment.yaml) workflow runs
`make ee` — the same command documented above — so the documented path is the tested path.

It triggers on pushes and pull requests that touch anything the image is built from
(`antsibull-nox.toml`, `noxfile.py`, `tests/ee/**`, `plugins/**`, `galaxy.yml`,
`meta/runtime.yml`, `pyproject.toml`, `Makefile`), weekly on Sundays to catch drift in the
base image and in the collections pulled from Galaxy, and on demand via
**Actions → Execution Environment → Run workflow**.

Each run writes a job summary listing the image tag, its size, the `ansible-core` version
and every collection installed inside it, so you can see what the image actually contains
without pulling it.

Note that the workflow does not trigger on `roles/**`. The roles ship inside the image but
the smoke test does not exercise them, and role changes are already covered by the Molecule
workflows.

## Where things live

| Path | Purpose |
|---|---|
| `antsibull-nox.toml` | The execution environment definition |
| `noxfile.py` | Loads the above; defines the `ee-check` session |
| `tests/ee/all.yml` | The smoke test run inside the built image |
| `ansible-navigator.yml` | Navigator settings; chiefly, it stops every run dropping a playbook artifact next to the test |
| `Makefile` (`ee` target) | The entry point |

None of these ship in the collection tarball; they are build tooling and are excluded via
`build_ignore` in `galaxy.yml`.
