# Playbooks

## Getting started
This playbooks folder has several sub folders.
Depending on what you are looking for, dive into the folders
and see the respective READMEs.

Name | Description
--- | ---
[demo](./demo/)|Contains demo playbooks that showcase functionality of this collection in a generic way.
[usecases](./usecases/)|Contains playbooks for specific use cases.
[vars](./vars/)|Contains variable files. We ship a `config.yml.example` for you to copy and several files for the [demo](./demo/) folder.
[roles.yml](./roles.yml)|Run the roles contained in this collection. Use the tags `agent` and `server` to limit the run to one role. Primarily used for testing.