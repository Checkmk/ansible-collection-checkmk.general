# Files
This folder is currently used to provide files to the `ansible-test` container
on GitHub Action execution. Primarily this currently concerns secrets for which
there is no other way of providing them to the container.
The folder `includes` contains shared resources, which are required by all tests.
**Please do not store anything in here unless you know, what you are doing!**
