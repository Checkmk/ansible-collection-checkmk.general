---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: robin-checkmk

---

Verify first that your issue is not already reported [here](https://github.com/tribe29/ansible-collection-tribe29.checkmk/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc).
Where possible also test if the latest release and main branch are affected too.
Complete all sections as described!

**Describe the bug**
<!--  A clear and concise description of what the bug is. -->

**Component Name**
<!--  Write the short name of the module or plugin below, use your best guess if unsure. -->
e.g. `activation`

**Ansible Version**
<!-- Paste verbatim output from `ansible --version` between triple backticks. -->
```console
$ ansible --version

```

**Checkmk Version and Edition**
<!-- Paste the version string, that can be found in the 'Help' menu. Please make sure to include the edition!-->
```console
e.g. 2.X.YpZ (CRE)
```

**Collection Version**
<!-- Paste verbatim output from`ansible-galaxy collection list` between triple backticks. -->
```console
$ ansible-galaxy collection list

```

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Run '....'
3. Execute '....'
4. See error

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->

**Actual behavior**
<!-- A clear and concise description of what actually happens. -->

**Minimum reproduction example**
<!-- If you can, please provide a minimum example of your configuration. This really helps us quickly understand the situation. -->
```yaml

```

**Additional context**
<!-- Add any other context, e.g. OS information about control and managed node, screenshots or background information about the problem. -->
