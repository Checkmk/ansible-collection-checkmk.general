#!/usr/bin/env bash
#
# Written by: Robin Gierse - robin.gieres@checkmk.com - on 20231027
#
# Purpose:
# Run tests locally.
#
# Usage:
#   Run Sanity Tests:                                     ./testing.sh -s
#   Run Integration Tests:                                ./testing.sh -i -t host
#   Run Unit Tests:                                       ./testing.sh -u -t tests/unit/plugins/inventory/test_checkmk.py
#   Run Linting:                                          ./testing.sh -l
#   Run QA (optionally with "-t" to specify a directory): ./testing.sh -q -t plugins
#   Run Molecule for server role and Checkmk 2.2.0:       ./testing.sh -m -r server -v 2.2.0

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
collection_dir="${script_dir%/*}"

mode="sanity"

while getopts 'squilmt:r:v:' OPTION; do
  case "$OPTION" in
    s)
      mode="sanity" ;;
    q)
      mode="qa" ;;
    u)
      mode="unit" ;;
    i)
      mode="integration" ;;
    l)
      mode="lint" ;;
    m)
      mode="molecule" ;;
    t)
      target="$OPTARG" ;;
    r)
      role="$OPTARG" ;;
    v)
      version="$OPTARG" ;;
    ?)
      echo "Unknown option!"
      exit 1
      ;;
  esac
done

_run_sanity() {
    echo "## Running Ansible Sanity Tests."
    uv run ansible-test sanity --docker
    echo "## Ansible Sanity Tests done."
}

_run_qa() {
    echo "## Running black for <${target:-plugins}> directory."
    uv run black --check --diff "${collection_dir}/${target:-plugins}/"
    echo "## black done."
    echo "## Running isort for <${target:-plugins}> directory."
    uv run isort --check --diff "${collection_dir}/${target:-plugins}/"
    echo "## isort done."
}

_run_integration() {
    if [ -n "${target}" ]; then
    echo "## Running Ansible Integration Tests for <${target}> Module."
    uv run ansible-test integration "${target}" --docker
    else
    echo "## Running Ansible Integration Tests for all Modules."
    uv run ansible-test integration --docker
    fi
    echo "## Ansible Integration Tests done."
}

_run_unit() {
    if [ -n "${target}" ]; then
    echo "## Running Ansible Unit Tests for <${target}>."
    uv run ansible-test units "${target}" --docker
    else
    echo "## Running Ansible Unit Tests for all Modules."
    uv run ansible-test units --docker
    fi
    echo "## Ansible Integration Tests done."
}

_run_linting() {
    echo "## Running yamllint."
    uv run yamllint -c "${collection_dir}/.yamllint" "${collection_dir}/roles/"
    uv run yamllint -c "${collection_dir}/.yamllint" "${collection_dir}/playbooks/"
    uv run yamllint -c "${collection_dir}/.yamllint" "${collection_dir}/tests/"
    echo "## yamllint done."
    echo "## Running ansible-lint."
    uv run ansible-lint -c "${collection_dir}/.ansible-lint" "${collection_dir}/roles/"
    uv run ansible-lint -c "${collection_dir}/.ansible-lint" "${collection_dir}/playbooks/"
    uv run ansible-lint -c "${collection_dir}/.ansible-lint" "${collection_dir}/tests/"
    echo "## ansible-lint done."
}

_run_molecule() {
    echo "## Running Molecule for ${role} role and Checkmk ${version}."
    cd "./roles/${role}/" || exit 1
    uv run molecule test -s "${version}"
    cd - || exit 1
    echo "## Molecule done."
}

case "$mode" in
    sanity)
        _run_sanity ;;
    qa)
        _run_qa ;;
    unit)
        _run_unit ;;
    integration)
        _run_integration ;;
    lint)
        _run_linting ;;
    molecule)
        _run_molecule ;;
    ?)
      echo "Unknown mode!"
      exit 1
      ;;
esac
