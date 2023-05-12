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
# - Checkmk versionen prüfen!

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
collection_dir="${script_dir%/*}"

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

echo "# Test findings:"
if [[ $(find "${collection_dir}/changelogs/fragments" | wc -l) -lt 1 ]] ; then echo "Make sure to provide all relevant changelogs!" ; fi
grep -R release_summary "${collection_dir}/changelogs/fragments/" > /dev/null || echo "Please provide a 'release_summary' in the changelogs!"
echo "# End tests section."

echo "# Changes:"
sed -i "s/version: ${source_version}/version: ${target_version}/g" "${collection_dir}/galaxy.yml" && echo "Updated Collection version in 'galaxy.yml' from ${source_version} to ${target_version}."
sed -i "s/version: ${source_version}/version: ${target_version}/g" "${collection_dir}/requirements.yml" && echo "Updated Collection version in 'requirements.yml' from ${source_version} to ${target_version}."
echo "# End changes section."