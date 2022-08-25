# Contributing

## Getting Started

General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).
See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for more details on how to contribute to collections in particular.

## A word of warning

While we want the community to engage in developing this collection, please be
aware, that we have to ensure a certain level of quality and scope.
Additionally, this is purely a side project of a few people, which means
the time available is limited. We will try to be as transparent as possible
about what we will include but please do not feel discouraged, if an idea
or proposal gets rejected. Instead go on and create something yourself,
if you think your approach is viable! There is already a lot of great content
out there and we love seeing you add to that plethora of it!

## How to contribute

There is several ways in which you can contribute:

1. Submit an [issue](#Submitting-Issues).
2. Create a [pull request](#Pull-Requests).

Everything helps, really!
We do test everything to the best of our abilities, but nothing beats real world
scenarios. Also if you can provide a bugfix yourself or you have an addition to
the functionality, [pull requests](#Pull-Requests) are appreciated.

### Submitting Issues

If you encounter any bugs or have ideas for improvements feel free to open an [issue](https://github.com/tribe29/ansible-collection-tribe29.checkmk/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) or even better a [pull request](#Pull-Requests).
Dedicated requirements will be added here as suitable.

### Pull Requests

Please open a [pull request](https://github.com/tribe29/ansible-collection-tribe29.checkmk/pulls?q=is%3Apr+is%3Aopen)
if you have something to contribute.
On pull request creation, checks will run and tell you,
if your changes work with the collection. If errors are detected, please try to
fix them and update your pull request accordingly.
If you need help, do ask for it.

### Changelog

When changing this collection, please make sure to write a log of what you did.
To do so, create a `.yml` file in the folder `changelogs/fragments`.
The name does not matter, as the changelog is compiled of all fragments
during build-time. For reference regarding the file format, you can take a look
at files in the folder `changelogs/archive`.

### Documentation

Documentation is still a work in progress.
Module documentation is compiled during a release and stored as `docs/module.rst`,
but this is not ideal yet. However, please use the inline documentation as seen
in the existing modules when creating additional modules.

## Style Guide

### Commit messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* The first line is a short title (limit to 72 characters or less)
* Write [good commit messages](https://chris.beams.io/posts/git-commit/)

### Plugins
Specifics to be done. Stick to general Ansible coding best practices and look out for sanity check gotchas.

### Roles
The following are guidelines to keep in mind, when changing roles.
- Variables
    - Use snake case (`snake_case_variable`)
    - Do not prefix the variable with an underscore ( `_` )
- Tags
    - When tagging roles, separate single words with dashes (`my-custom-tag`)

## Releasing this collection
Releasing this collection is automated using GitHub Actions.
Before running the action `Release Collection` against the `main` branch, the
following needs to be done:

1. Update the collection version in `galaxy.yml`. Look for `version:`.
2. Double check `changelogs/fragments` if all changes have a changelog.
3. After all changes have been performed, merge them into the `main` branch.
4. Release the collection by running the action `Release Collection` against the `main` branch.
5. Merge the automatically created pull request and update the `devel` branch from `main`.

## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).

## Forum

If you have questions, feedback and or simply no Github account feel free to
reach out to our awesome [Checkmk Community (using the 'ansible' tag)](https://forum.checkmk.com/tag/ansible).
