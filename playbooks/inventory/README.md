# Inventory

This directory contains configuration examples for the Checkmk inventory plugin, which allows you to use your Checkmk monitoring site as a dynamic inventory source for Ansible.

## Contents

* `checkmk.yml`: An example inventory configuration file that uses the `checkmk.general.checkmk` plugin to retrieve hosts and their attributes from your Checkmk site.
* `hosts.ini`: Contains hosts for local collection testing, based on the `Vagrantfile` from the project root.

## Usage

To use the inventory source, you must configure your Checkmk site connection details (URL, site, user, and secret) in the `checkmk.yml` file or pass them via environment variables.

You can verify the inventory and view the host graph by running the following command:

    ansible-inventory -i checkmk.yml --graph

For more details, run the following command:

    ansible-doc -t inventory checkmk.general.checkmk
