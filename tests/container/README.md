# Custom Docker Containers for Integration Tests
## Why
TBD

## How-to
- `docker build -t ansible-checkmk-test ./`
- `ansible-test integration activation --docker-privileged --python 3.10 --docker ansible-checkmk-test`

## Recognition
This project uses https://github.com/gdraheim/docker-systemctl-replacement.
