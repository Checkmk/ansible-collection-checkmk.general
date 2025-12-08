# Playbook Variables

This directory contains variable files used by the playbooks in the `demo` and `usecases` directories.

## Contents

* **Global Variables**: Configuration files defining common variables such as Checkmk server connection details (`server_url`, `site`, `automation_user`, `automation_secret`).
* **Scenario-Specific Variables**: Variable files tailored for specific test cases or demonstration scenarios.

## Usage

These files are typically included in playbooks using the `vars_files` keyword or automatically loaded by Ansible depending on your configuration.
