# tribe29 documentation

## Development process

When making changes to the collection please keep in mind to add a new file to
the `changelogs/fragments` folder in which you document, what you are changing.
The changelog will be built automatically on github.
If uncertain, ask @robin-tribe29 about how to handle the changelogs.

## Tests

Always run tests! The following are currently implemented:

- `ansible-test sanity --docker default`
- `ansible-test integration --docker default`

Changes should only be pushed, when all tests succeed locally.
Additionally those tests are run using Github Actions.

## Release

The release process is really straight forward: Update `galaxy.yml` with the
new version number, check the changelogs and tests and then run
the Github Action `Release Collection`. That takes care of creating a release
on Github and publishing the artifact to the Ansible Galaxy.

## Ressources
- https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html
- https://docs.ansible.com/ansible/latest/user_guide/collections_using.html
