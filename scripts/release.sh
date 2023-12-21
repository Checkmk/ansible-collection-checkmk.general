#!/usr/bin/env bash
#
# Written by: Robin Gierse - robin.gieres@checkmk.com - on 20230502
#
# Purpose:
# Prepare this repository for a release.
#
# Usage: ./release.sh -s 0.21.0 -t 0.22.0
#

# ToDo
# - Collection version prüfen!

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
collection_dir="${script_dir%/*}"

# Update these as necessary:
checkmk_ancient="2.0.0p39"
checkmk_oldstable="2.1.0p37"
checkmk_stable="2.2.0p17"

while getopts 's:t:' OPTION; do
  case "$OPTION" in
    s)
      source_version="$OPTARG" ;;
    t)
      target_version="$OPTARG" ;;
    ?)
      echo "Unknown option!"
      exit 1
      ;;
  esac
done

echo "# General things to keep in mind:"
echo "- Did you provide changelogs for all relevant changes?"
echo "- Did you update SUPPORT.md with the latest compability information?"
echo

echo "# Changes:"
sed -i "s/version: ${source_version}/version: ${target_version}/g" "${collection_dir}/galaxy.yml" && echo "Updated Collection version in 'galaxy.yml' from ${source_version} to ${target_version}."
# The following is quite hacky, but it works well enough. If you want to tame the sed monster, have at it. Otherwise be careful with changes here.
## Integration tests
find "${collection_dir}/tests/integration/targets/" -type f -name main.yml -exec sed -i "s/2.2.0.*/${checkmk_stable}\"/g" {} \; && echo "Updated Checkmk Stable version for integration tests to ${checkmk_stable}."
find "${collection_dir}/tests/integration/targets/" -type f -name main.yml -exec sed -i "s/2.1.0.*/${checkmk_oldstable}\"/g" {} \; && echo "Updated Checkmk Oldstable version for integration tests to ${checkmk_oldstable}."
find "${collection_dir}/tests/integration/targets/" -type f -name main.yml -exec sed -i "s/2.0.0.*/${checkmk_ancient}\"/g" {} \; && echo "Updated Checkmk Ancient version for integration tests to ${checkmk_ancient}."
## Molecule tests
find "${collection_dir}/roles/" -type f -name all.yml -exec sed -i "s/2.2.0.*/${checkmk_stable}\"/g" {} \; && echo "Updated Checkmk Stable version for molecule tests to ${checkmk_stable}."
find "${collection_dir}/roles/" -type f -name all.yml -exec sed -i "s/2.1.0.*/${checkmk_oldstable}\"/g" {} \; && echo "Updated Checkmk Oldstable version for molecule tests to ${checkmk_oldstable}."
find "${collection_dir}/roles/" -type f -name all.yml -exec sed -i "s/2.0.0.*/${checkmk_ancient}\"/g" {} \; && echo "Updated Checkmk Ancient version for molecule tests to ${checkmk_ancient}."
# Roles:
find "${collection_dir}/roles/" -type f -name main.yml -exec sed -i "s/2.2.0.*/${checkmk_stable}\"/g" {} \; && echo "Updated default Checkmk version for roles to ${checkmk_stable}."
find "${collection_dir}/roles/" -type f -name README.md -exec sed -i "s/2.2.0.*/${checkmk_stable}\"/g" {} \; && echo "Updated default Checkmk version in roles README to ${checkmk_stable}."
# Support Matrix
grep "${target_version}" "${collection_dir}/SUPPORT.md" || echo "${target_version} | ${checkmk_ancient}, ${checkmk_oldstable}, ${checkmk_stable} | 2.14, 2.15, 2.16 | None" >> "${collection_dir}/SUPPORT.md" && echo "Added line to compatibility matrix in SUPPORT.md."

echo "# End changes section."
echo

echo "# Test findings:"
if [[ $(find "${collection_dir}/changelogs/fragments" | wc -l) -lt 1 ]] ; then echo "Make sure to provide all relevant changelogs!" ; fi
grep -R release_summary "${collection_dir}/changelogs/fragments/" > /dev/null || echo "Please provide a 'release_summary' in the changelogs!"
grep "${target_version}" "${collection_dir}/SUPPORT.md" > /dev/null || echo "Please provide a line about the version support in 'SUPPORT.md'!"
echo "# End tests section."
