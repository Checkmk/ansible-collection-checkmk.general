#!/usr/bin/env bash
#
# Written by: Robin Gierse - robin.gieres@checkmk.com - on 20231027
#
# Purpose:
# Run tests locally.
#
# Usage:
#   Run Sanity Tests:                               ./testing.sh -s
#   Run Integration Tests:                          ./testing.sh -i -t host
#   Run Linting:                                    ./testing.sh -l
#   Run QA:                                         ./testing.sh -q
#   Run Molecule for server role and Checkmk 2.2.0: ./testing.sh -m -r server -v 2.2.0

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
collection_dir="${script_dir%/*}"

mode="sanity"

while getopts 'sqilmt:r:v:' OPTION; do
  case "$OPTION" in 
    s) 
      mode="sanity" ;;
    q) 
      mode="qa" ;;
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
    ansible-test sanity --docker
    echo "## Ansible Sanity Tests done."
}

_run_qa() {
    echo "## Running black."
    black --check --diff "${collection_dir}/plugins/"
    echo "## black done."
    echo "## Running isort."
    isort --check --diff "${collection_dir}/plugins/"
    echo "## isort done."
}

_run_integration() {
    if [ -n "${target}" ]; then
    echo "## Running Ansible Integration Tests for <${target}> Module."
    ansible-test integration "${target}" --docker
    else
    echo "## Running Ansible Integration Tests for all Modules."
    ansible-test integration --docker
    fi
    echo "## Ansible Integration Tests done."
}

_run_linting() {
    echo "## Running yamllint."
    yamllint -c "${collection_dir}/.yamllint" "${collection_dir}/roles/"
    yamllint -c "${collection_dir}/.yamllint" "${collection_dir}/playbooks/"
    echo "## yamllint done."
    echo "## Running ansible-lint."
    ansible-lint -c "${collection_dir}/.ansible-lint" "${collection_dir}/roles/"
    ansible-lint -c "${collection_dir}/.ansible-lint" "${collection_dir}/playbooks/"
    echo "## ansible-lint done."
}

_run_molecule() {
    echo "## Running Molecule for ${role} role and Checkmk ${version}."
    cd "./roles/${role}/" || exit 1
    molecule test -s "${version}"
    cd - || exit 1
    echo "## Molecule done."
}

case "$mode" in 
    sanity) 
        _run_sanity ;;
    qa) 
        _run_qa ;;
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
