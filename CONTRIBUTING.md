# Contributing

## Getting Started

General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).
See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for more details on how to contribute to collections in particular.

## A word of warning

While we want the community to engage in developing this collection, please be
aware, that we also want to ensure a certain level of quality and scope.
Additionally, this is purely a side project of a few people, which means
the time available is limited. We will try to be as transparent as possible
about what we will include but please do not feel discouraged, if an idea
or proposal gets rejected. Instead go on and create something yourself,
if you think your approach is viable! There is already a lot of great content
out there and we love seeing you add to that plethora!

## How to contribute

There are several ways in which you can contribute:

1. Submit an [issue](#Submitting-Issues).
2. Create a [pull request](#Pull-Requests).
3. Pick an [issue, which needs help](https://github.com/Checkmk/ansible-collection-checkmk.general/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).

Everything helps, really!
Not only issues and code, but also documentation and
just spreading the word about this collection goes a long way!

### Submitting Issues

If you encounter any bugs or have ideas for improvements feel free to open an [issue](https://github.com/Checkmk/ansible-collection-checkmk.general/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) or even better a [pull request](#Pull-Requests).
Please use the existing templates, especially for bug reports, as that helps you
and us to gather the necessary information to tackle the issue efficiently.

### Pull Requests

Please open a [pull request](https://github.com/Checkmk/ansible-collection-checkmk.general/pulls?q=is%3Apr+is%3Aopen)
against the `devel` branch, if you have something to contribute. It does not matter, if that is
a cool new feature, a bug fix or documentation, we appreciate everything you want to contribute!
On pull request creation, checks will run and tell you, if your changes work with the collection.
If errors are detected, please try to fix them and update your pull request accordingly.
If you need help, do ask for it.
After submitting a PR, follow the instructions to sign the [CLA](https://github.com/Checkmk/checkmk/blob/master/doc/cla/cla_readme.md) as asked by the bot.

### Changelog

When changing this collection, please make sure to write a log of what you did.
To do so, create a `.yml` file in the folder `changelogs/fragments/`.
The name does not matter, as the changelog is compiled of all fragments
during build-time. For reference regarding the file format, take a look
at the file `changelogs/template.yml`.

### Documentation

Module documentation is compiled during a release and stored as `docs/module.rst`.
It also becomes available [in the Galaxy](https://galaxy.ansible.com/ui/repo/published/checkmk/general/docs/).
Please use the inline documentation as seen in the existing modules when creating additional modules.

## Style Guide

### Commit messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* The first line is a short title (limit to 72 characters or less)
* Write [good commit messages](https://chris.beams.io/posts/git-commit/)

### Plugins

In general, stick to Ansible coding best practices and look out for test gotchas.

**Module Options**

There are different approaches to the module options, depending on the nature of the module:

**Approach 1**: The module only interacts with one class of objects. For example the `host_group` module only ever interacts with host groups. Hence the module options should stay as simple as possible, e.g. `name` instead of `host_group_name` for the name of the host group.

**Approach 2**: The module interacts with more than one class of objects. For example the `downtime` module can interact both with hosts and with services. Hence the module options need to be more precise than in *Approach 1*. For example `host_name` and `service_description` instead of just `name`, as that would not make clear with which class ob objects we are interacting.

**Aliases**

It is possible to implement an alias for a module option. This should be used rather carefully to not clutter the options. However, they can be an option, if one is uncertain how to name an option, or to deprecate an option, before actually removing it. If in doubt, feel free to ask for review in your PR.

### Roles and Playbooks

The following are guidelines to keep in mind, when creating or changing roles and playbooks.
- Variables
    - Use snake case (`snake_case_variable`)
    - Name variables after their purpose.
        - `checkmk_server_foo` for a server role variable
        - `checkmk_agent_bar` for a agent role variable
        - `checkmk_var_bat` for general variables
    - Internal variables, not intended to be changed by a user should be prefixed with a double underscore (`__`).
- Tags
    - When tagging roles or playbooks, separate single words with dashes (`my-custom-tag`)

## Tests

We strive to provide the best possible quality with this collection, hence we have implemented tests, that verify different aspects of code quality.
We urge you to run the following tests locally as applicable, so the turnaround on your pull request is as low as possible.

If you are developing a plugin or module yourself, please try to create
unit and integration tests for them as well. You can refer to existing tests as inspiration.

### Sanity

[Ansible Sanity Tests](https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html) enforce Ansible coding standards and requirements facilitating static code analysis. The `ansible-test` tool typically comes along with your Ansible installation (e.g. if you use the `requirements.txt` of this project).
We recommend using the `--docker` option, so you get the best results, as that uses a Docker image crafted and maintained by the Ansible project.
**Caution**: By default, Docker containers cannot be run as an unprivileged user! Depending on your setup you need to allow your user to run containers, or run `ansible-test` with `sudo`. Keep in mind, that with the latter you are running in another environment and might need to take care of installing the Python requirements for Ansible.

To run the tests locally, use the following command in the project root:

    ansible-test sanity --docker

You can also run a subset by mentioning them as follows. See `ansible-test sanity --list-tests` for available tests. We strongly recommend to run all tests though.

    ansible-test sanity $TEST_CASE --docker

### Integration

[Ansible Integration Tests](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html) run test cases created by the maintainers of the respective modules, to ensure the collection actually does what is intended. The `ansible-test` tool typically comes along with your Ansible installation (e.g. if you use the `requirements.txt` of this project).
We strongly recommend using the `--docker` option, so you do not modify your local system with these tests.
**Caution**: By default, Docker containers cannot be run as an unprivileged user! Depending on your setup you need to allow your user to run containers, or run `ansible-test` with `sudo`. Keep in mind, that with the latter you are running in another environment and might need to take care of installing the Python requirements for Ansible.

To run all tests locally, use the following command in the project root:

    ansible-test integration --docker

You can also run a subset by mentioning them as follows. See `tests/integration/targets` for potential test targets).

    ansible-test integration $TEST_CASE --docker

### Unit

[Ansible Unit Tests](https://docs.ansible.com/ansible/latest/dev_guide/testing_unit.html) run unit tests created by the maintainers of the respective modules, to ensure the code works as intended. The `ansible-test` tool typically comes along with your Ansible installation (e.g. if you use the `requirements.txt` of this project).
We strongly recommend using the `--docker` option, so you do not modify your local system with these tests.
**Caution**: By default, Docker containers cannot be run as an unprivileged user! Depending on your setup you need to allow your user to run containers, or run `ansible-test` with `sudo`. Keep in mind, that with the latter you are running in another environment and might need to take care of installing the Python requirements for Ansible.

To run all tests locally, use the following command in the project root:

    ansible-test units --docker

You can also run a subset by mentioning them as follows. See `tests/unit/plugins` for potential test targets).

    ansible-test units --docker tests/unit/plugins/inventory/test_checkmk.py

### Molecule

To test our roles, we use [Molecule](https://www.jeffgeerling.com/blog/2018/testing-your-ansible-roles-molecule). It can be installed using the `requirements.txt` in this project or manually. The tests are crafted by the maintainers of the respective role to reflect real world scenarios a role would be used in. To run the tests, you need to navigate to the role directory and choose a scenario. At the time of writing those are named after the supported Checkmk versions: `2.2.0`and `2.3.0`.

    cd roles/server/
    molecule test -s 2.2.0
    molecule test -s 2.3.0

## Releasing this collection

Releasing this collection is automated using GitHub Actions.
Before running the action `Release Collection` against the `main` branch, the
following needs to be done:

1. Create a pull request from `devel` into `main` with the following naming scheme: `Release X.Y.Z`.
2. Choose and note which feature pull request you want to include in this release.
3. Check the GitHub Workflows for [EOL Ansible and Python versions and add new releases](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix).
4. The following tasks are automated in `scripts/release.sh`. Feel free to use the script, but double-check the result!
    1. Update the collection version in `galaxy.yml` and `requirements.yml`. Look for the string `version:`.
    2. Check the integration and molecule tests for up-to-date Checkmk versions and update if necessary.
    3. Update the compatibility matrix in `SUPPORT.md` accordingly.
5. Double check `changelogs/fragments` if all changes have a changelog.
6. After all changes have been performed, merge them into the `main` branch.
7. Release the collection by running the action `Release Collection` against the `main` branch.
8. Merge the automatically created pull request into `devel` and then update the `main` branch from `devel`.

Some of these steps can already be checked and done with `scripts/release.sh`.
This is a work in progress and should be used carefully.
You should definitely check the resulting changes thoroughly before committing.

## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).

## Forum

If you have questions, feedback and or simply no Github account feel free to
reach out to our awesome [Checkmk Community (using the 'ansible' tag)](https://forum.checkmk.com/tag/ansible).
