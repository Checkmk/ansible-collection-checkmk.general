#!/usr/bin/env bash
#
# Written by: Robin Gierse - robin.gierse@checkmk.com - on 20230502
#
# Purpose:
# Prepare this repository for a release.
#
# Usage: ./release.sh -s 9.0.0 -t 9.2.1

set -euo pipefail

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
collection_dir="${script_dir%/*}"

## Configuration
# The Checkmk branches this collection supports.
checkmk_branch_ancient="2.3.0"
checkmk_branch_oldstable="2.4.0"
checkmk_branch_stable="2.5.0"

# The Ansible versions this collection is tested against, as listed in SUPPORT.md.
# Keep this in sync with the matrix in '.github/workflows/' and 'meta/runtime.yml'.
ansible_versions="2.19, 2.20, 2.21"

# The manifest of released Checkmk versions. It is cached between runs, but refreshed
# once it is older than the maximum age below. Delete the file to force a refresh.
manifest_url="https://download.checkmk.com/stable_downloads.json"
manifest_file="/tmp/stable_downloads.json"
manifest_max_age_minutes="1440"  # 1440 minutes = 1 day

usage() {
  echo "Usage: ${0##*/} -s <source_version> -t <target_version>" >&2
  echo "Example: ${0##*/} -s 9.0.0 -t 9.2.1" >&2
}

source_version=""
target_version=""

while getopts 's:t:' OPTION; do
  case "$OPTION" in
    s)
      source_version="$OPTARG" ;;
    t)
      target_version="$OPTARG" ;;
    ?)
      usage
      exit 1
      ;;
  esac
done

if [ -z "${source_version}" ] || [ -z "${target_version}" ]; then
  echo "Both the source version (-s) and the target version (-t) are required!" >&2
  usage
  exit 1
fi

echo "# Preparations:"

wget -V > /dev/null 2>&1 || { echo "Please install <wget>." >&2 ; exit 1 ; }
jq -h > /dev/null 2>&1 || { echo "Please install <jq>." >&2 ; exit 1 ; }

manifest_is_current() {
  # A cached manifest is only reused as long as it is recent enough.
  [ -f "${manifest_file}" ] || return 1
  [ -z "$(find "${manifest_file}" -maxdepth 0 -mmin "+${manifest_max_age_minutes}")" ]
}

download_manifest() {
  # Downloads to a temporary file and only moves it into place once it is complete.
  local tmp_manifest
  tmp_manifest="$(mktemp "${manifest_file}.XXXXXX")"
  if ! wget --quiet --tries=3 --timeout=30 -O "${tmp_manifest}" "${manifest_url}" ; then
    rm -f "${tmp_manifest}"
    echo "Could not download the Checkmk versions manifest from ${manifest_url}!" >&2
    exit 1
  fi
  mv "${tmp_manifest}" "${manifest_file}"
}

get_checkmk_version() {
  # Reads the latest patch version of a Checkmk branch from the manifest.
  local branch="$1" version
  version="$(jq -r --arg branch "${branch}" '.checkmk[$branch].version // empty' < "${manifest_file}")"
  if [ -z "${version}" ]; then
    echo "Could not determine the latest version of Checkmk ${branch} from the manifest!" >&2
    echo "Check the branches used in this script against ${manifest_url}." >&2
    exit 1
  fi
  echo "${version}"
}

if manifest_is_current ; then
  echo "Using cached Checkmk versions manifest."
else
  echo "Downloading latest Checkmk versions manifest."
  download_manifest
fi

warnings=()

warn() {
  # Records something the script could not do, to be repeated in the summary at the end.
  warnings+=("$1")
  echo "WARNING: $1" >&2
}

replace_checkmk_version() {
  # Replaces the version of a Checkmk branch in the given files.
  # Only versions that are a YAML value ('key: 2.5.0p1', 'key: "2.5.0p1"') or a list
  # item ('- 2.5.0p1') are replaced, and only the version itself. Prose mentioning a
  # version and everything following the version on the line are left untouched.
  # The replacement is only reported as done if there was actually something to replace.
  local description="$1" branch="$2" version="$3"
  local branch_re="${branch//./\\.}"
  shift 3
  if [ "$#" -eq 0 ] ; then
    warn "Found no files at all for ${description}, so nothing was updated!"
    return 0
  fi
  local pattern="((:|-)[[:space:]]+['\"]?)${branch_re}[a-z0-9]*"
  if ! grep -qE "${pattern}" "$@" ; then
    warn "Found no Checkmk ${branch} version in ${description}, so nothing was updated!"
    return 0
  fi
  sed -i -E "s/${pattern}/\1${version}/g" "$@"
  echo "Updated ${description} to ${version}."
}

replace_collection_version() {
  # Replaces a whole line containing the collection version and only reports success
  # if that line was actually found.
  local description="$1" file="$2" old_line="$3" new_line="$4"
  if grep -qxF "${new_line}" "${file}" ; then
    echo "Left ${description} alone, it is already at ${target_version}."
    return 0
  fi
  if ! grep -qxF "${old_line}" "${file}" ; then
    warn "Found no line '${old_line}' in ${file#"${collection_dir}/"}, so ${description} was not updated!"
    return 0
  fi
  # The line was matched as a fixed string above, only the dots need escaping here.
  sed -i "s|^${old_line//./\\.}$|${new_line}|" "${file}"
  echo "Updated ${description} from ${source_version} to ${target_version}."
}

checkmk_ancient="$(get_checkmk_version "${checkmk_branch_ancient}")"
checkmk_oldstable="$(get_checkmk_version "${checkmk_branch_oldstable}")"
checkmk_stable="$(get_checkmk_version "${checkmk_branch_stable}")"

echo "Checkmk Ancient: $checkmk_ancient"
echo "Checkmk Oldstable: $checkmk_oldstable"
echo "Checkmk Stable: $checkmk_stable"
echo

echo "# General things to keep in mind:"
echo "- Did you provide changelogs for all relevant changes?"
echo "- The compatibility matrix in SUPPORT.md is updated below, but remarks are up to you."
echo

echo "# Changes:"
echo "## Collection version"
replace_collection_version "the Collection version in 'galaxy.yml'" "${collection_dir}/galaxy.yml" \
  "version: ${source_version}" "version: ${target_version}"
replace_collection_version "the Collection version in 'pyproject.toml'" "${collection_dir}/pyproject.toml" \
  "version = \"${source_version}\"" "version = \"${target_version}\""
echo

echo "## Checkmk version in the roles"
mapfile -t role_files < <(find "${collection_dir}/roles/" -type f \( -path "*/defaults/main.yml" -o -path "*/meta/argument_specs.yml" \))
replace_checkmk_version "the default Checkmk version for roles" "${checkmk_branch_stable}" "${checkmk_stable}" "${role_files[@]}"
mapfile -t role_readme_files < <(find "${collection_dir}/roles/" -type f -name README.md)
replace_checkmk_version "the default Checkmk version in the roles README" "${checkmk_branch_stable}" "${checkmk_stable}" "${role_readme_files[@]}"
echo

echo "## Checkmk version in the playbooks"
replace_checkmk_version "the default Checkmk version for playbooks" "${checkmk_branch_stable}" "${checkmk_stable}" "${collection_dir}/playbooks/vars/auth.yml"
echo

echo "## Checkmk versions in the integration tests"
replace_checkmk_version "the Checkmk Stable version for integration tests default (setup_checkmk)" "${checkmk_branch_stable}" "${checkmk_stable}" "${collection_dir}/tests/integration/targets/setup_checkmk/defaults/main.yml"
replace_checkmk_version "the Checkmk Stable version for the integration_config.yml.template example" "${checkmk_branch_stable}" "${checkmk_stable}" "${collection_dir}/tests/integration/integration_config.yml.template"
echo

echo "## Checkmk versions in the molecule tests"
mapfile -t molecule_files < <(find "${collection_dir}/roles/" -type f -path "*/molecule/*/group_vars/all.yml")
replace_checkmk_version "the Checkmk Stable version for molecule tests" "${checkmk_branch_stable}" "${checkmk_stable}" "${molecule_files[@]}"
replace_checkmk_version "the Checkmk Oldstable version for molecule tests" "${checkmk_branch_oldstable}" "${checkmk_oldstable}" "${molecule_files[@]}"
replace_checkmk_version "the Checkmk Ancient version for molecule tests" "${checkmk_branch_ancient}" "${checkmk_ancient}" "${molecule_files[@]}"
echo

echo "## Checkmk versions in the GitHub Workflows"
mapfile -t workflow_files < <(find "${collection_dir}/.github/workflows/" -type f -name "ans-int-test-*.yaml")
replace_checkmk_version "the Checkmk Stable version for GitHub Workflows" "${checkmk_branch_stable}" "${checkmk_stable}" "${workflow_files[@]}"
replace_checkmk_version "the Checkmk Oldstable version for GitHub Workflows" "${checkmk_branch_oldstable}" "${checkmk_oldstable}" "${workflow_files[@]}"
replace_checkmk_version "the Checkmk Ancient version for GitHub Workflows" "${checkmk_branch_ancient}" "${checkmk_ancient}" "${workflow_files[@]}"
echo

echo "## Compatibility matrix"
if grep -q "${target_version}" "${collection_dir}/SUPPORT.md" ; then
  echo "Compatibility matrix in SUPPORT.md already mentions ${target_version}, leaving it alone."
else
  echo "${target_version} | ${checkmk_ancient}, ${checkmk_oldstable}, ${checkmk_stable} | ${ansible_versions}" >> "${collection_dir}/SUPPORT.md"
  echo "Added line to compatibility matrix in SUPPORT.md."
fi
echo

echo "# Test findings:"
if [[ $(find "${collection_dir}/changelogs/fragments" -type f -name '*.yml' | wc -l) -lt 1 ]] ; then echo "Make sure to provide all relevant changelogs!" ; fi
grep -R release_summary "${collection_dir}/changelogs/fragments/" > /dev/null || echo "Please provide a 'release_summary' in the changelogs!"
grep -R breaking_changes "${collection_dir}/changelogs/fragments/" > /dev/null && echo "Breaking changes found! Make sure to reflect this in the release version!"
if [ "${#warnings[@]}" -gt 0 ] ; then
  echo "The following changes could not be made, please check them manually:"
  printf -- "- %s\n" "${warnings[@]}"
fi
echo

# Make sure a release that was only prepared halfway does not look like a successful one.
[ "${#warnings[@]}" -eq 0 ]
