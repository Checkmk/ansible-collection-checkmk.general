# Contributing

## Getting Started

General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).

## A word of warning

While we want the community to engage in developing this collection, please be
aware, that we have to ensure a certain level of quality and scope.
Additionally, this is purely a side project of a few people, which means
the time available is limited. We will try to be as transparent as possible
about what we will include but please do not feel discouraged, if an idea
or proposal gets rejected. Instead go on and create something yourself,
if you think your approach is viable! There is already a lot of great content
out there and we love seeing you add to that plethora of content!

## Submitting Issues

If you encounter any bugs or have ideas for improvements feel free to open an [issue](https://github.com/tribe29/ansible-collection-tribe29.checkmk/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) or even better a [pull request](#Pull-Requests).
Dedicated requirements will be added here as suitable.

## Pull Requests

Please open a [pull request](https://github.com/tribe29/ansible-collection-tribe29.checkmk/pulls?q=is%3Apr+is%3Aopen)
if you have something to contribute.
On pull request creation, checks will run and tell you,
if your changes work with the collection. If errors are detected, please try to
fix them and update your pull request accordingly.
If you need help, feel free to ask for it.

## How to contribute

There is several ways in which you can contribute:

1. Submit an [issue](#Submitting-Issues).
2. Create a [pull request](#Pull-Requests).

Everything helps, really!
We do test everything to the best of our abilities, but nothing beats real world
scenarios. Also if you can provide a bugfix yourself or you have an addition to
the functionality, [pull request](#Pull-Requests) are appreciated.

### Changelog

When changing this collection, please make sure to write a log of what you did.
To do so, create a `.yml` file in the folder `changelogs/fragments`.
The name does not matter, as the changelog is compiled of all fragments
during build-time. For reference regarding the file format, you can take a look
at files in the folder `changelogs/archive`.

### Documentation

Documentation is still a work in progress.
For modules please use the inline documentation as seen in the existing modules.

## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).

## Forum

If you have questions, feedback and or simply no Github account feel free to
reach out to our awesome [Checkmk Community (using the 'ansible' tag)](https://forum.checkmk.com/tag/ansible).
