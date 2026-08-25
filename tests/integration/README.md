# Integration Tests

One target per module (`tests/integration/targets/<name>/`) or lookup
plugin (`tests/integration/targets/lookup_<name>/`). Every target depends
on the `setup_checkmk` role, which installs and starts the Checkmk site(s)
the tests run against.

## Running

```bash
uv run ansible-test integration --docker                        # full suite
uv run ansible-test integration <target> --docker                # single target, e.g. host
uv run ansible-test integration <target> <target2> --docker      # a few targets
uv run ansible-test integration --start-at <target> --docker     # resume after a failure
```

`--docker` must come last, after any target names.

By default this installs Checkmk into a single container and
creates a central site (`testsite`, port 5000) plus one
remote site (`testsite_r_1`, port 5001) - see
`tests/integration/targets/setup_checkmk/defaults/main.yml`.

## Podman: raise the task limit

With rootless podman, add this once - without it the tests fail:

```ini
# ~/.config/containers/containers.conf
[containers]
pids_limit = 0
```

Podman defaults to `pids_limit = 2048`. `systemd` is PID 1 inside the
ansible-test container and derives `DefaultTasksMax = 15% of that = 307`,
and everything `podman exec` starts - the whole `ansible-playbook` run
plus the Checkmk site it provisions - lands in `init.scope`. So the entire
test run shares 307 tasks. A site idles at ~180 of them, and the 3.0
ClickHouse metric backend alone wants 512 threads. CI uses Docker, which
sets no pids limit, so this never shows up there.

It has to be that file, not an environment variable: `ansible-test`'s
`common_environment()` passes only `HOME`, `PATH` and a short allowlist
through to podman, so `CONTAINERS_CONF_OVERRIDE` never arrives.

Symptoms, which vary with whichever process loses the race for the last
task slot and none of which name the real cause:

- `/bin/sh: 1: Cannot fork` - Ansible cannot start the module
- a bare Apache `500 Internal Server Error` from the site, with
  `RuntimeError: can't start new thread` in `var/log/apache/error_log`
- `Couldn't get 512 threads from global thread pool` in
  `var/log/clickhouse-server/clickhouse-server.err.log`

To confirm it, read `/sys/fs/cgroup/init.scope/pids.events` inside the
container: a rising `max` counter there is this limit. The container's own
`/sys/fs/cgroup/pids.events` stays at `max 0`, which is why the failure
looks like the host running out of memory.

## Testing a different version or edition

Copy the template and uncomment what you need:

```bash
cp tests/integration/integration_config.yml.template tests/integration/integration_config.yml
```

Then edit `checkmk_var_version` / `checkmk_var_edition` (and, if the
edition needs download credentials, `checkmk_var_download_user` /
`checkmk_var_download_pass`) in that file. `ansible-test` auto-loads it as
extra-vars, which override the role defaults. This file is gitignored —
don't commit it.
