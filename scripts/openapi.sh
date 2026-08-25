#!/usr/bin/env bash
#
# Written by: Robin Gierse - robin.gierse@checkmk.com - on 20260825
#
# Purpose:
# Extract the OpenAPI specification from a Checkmk site.
#
# Every site serves its own specification, so this is the way to get a spec that
# matches a particular Checkmk version exactly. The site has to be running.
#
# Usage:
#   Extract both variants into 'misc/':      ./openapi.sh -s mysite
#   Only the documentation variant:          ./openapi.sh -s mysite -f doc
#   Write somewhere else:                    ./openapi.sh -s mysite -o /tmp
#   Against a remote server:                 ./openapi.sh -s mysite -U https://myserver
#   With explicit credentials:               ./openapi.sh -s mysite -a myuser -p mysecret
#
# Credentials default to the ones 'cmk-dev-install-site' configures on a local
# development site. Override them with '-a' and '-p', or by exporting
# CHECKMK_VAR_API_USER and CHECKMK_VAR_API_SECRET.

set -euo pipefail

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
collection_dir="${script_dir%/*}"

## Configuration
# Defaults for a site created by 'cmk-dev-install-site'.
api_user="${CHECKMK_VAR_API_USER:-cmkadmin}"
api_secret="${CHECKMK_VAR_API_SECRET:-cmk}"
server_url="http://localhost"
output_dir="${collection_dir}/misc"
# 'doc' is the complete published API, 'swagger-ui' is what the built-in Swagger
# UI renders. Note that neither is the 'internal' variant of 'misc/spec.yaml',
# which is not served by any site and only comes out of the source tree.
variants="doc swagger-ui"

usage() {
  echo "Usage: ${0##*/} -s SITE [-f doc|swagger-ui|both] [-o DIR] [-U URL] [-a USER] [-p SECRET]"
  exit 1
}

while getopts 's:f:o:U:a:p:h' OPTION; do
  case "$OPTION" in
    s)
      site="$OPTARG" ;;
    f)
      case "$OPTARG" in
        doc|swagger-ui)
          variants="$OPTARG" ;;
        both)
          variants="doc swagger-ui" ;;
        *)
          echo "Unknown variant: ${OPTARG}" >&2 ; usage ;;
      esac ;;
    o)
      output_dir="$OPTARG" ;;
    U)
      server_url="${OPTARG%/}" ;;
    a)
      api_user="$OPTARG" ;;
    p)
      api_secret="$OPTARG" ;;
    h|?)
      usage ;;
  esac
done

[[ -n "${site:-}" ]] || usage
[[ -d "$output_dir" ]] || { echo "No such directory: ${output_dir}" >&2 ; exit 1 ; }

api_url="${server_url}/${site}/check_mk/api/1.0"

# The version endpoint doubles as a reachability and credentials check.
if ! version_json=$(curl -sSf -u "${api_user}:${api_secret}" "${api_url}/version" 2>&1); then
  echo "Cannot reach ${api_url}" >&2
  echo "Is the site running ('omd status ${site}') and are the credentials correct?" >&2
  exit 1
fi

# Example: "2.5.0p11.cee" or "2.5.0-2026.08.25.pro" - keep the leading X.Y.Z.
build=$(sed -n 's/.*"checkmk": *"\([^"]*\)".*/\1/p' <<< "$version_json")
[[ -n "$build" ]] || { echo "Could not determine the Checkmk version from:" >&2
                       echo "$version_json" >&2 ; exit 1 ; }
version=$(sed -E 's/^([0-9]+\.[0-9]+\.[0-9]+).*/\1/' <<< "$build")

echo "Site '${site}' runs Checkmk ${build}"

for variant in $variants; do
  target="${output_dir}/openapi-${variant}-${version}.yaml"
  if ! curl -sSf -u "${api_user}:${api_secret}" \
       "${api_url}/openapi-${variant}.yaml" -o "$target"; then
    echo "Failed to fetch the '${variant}' variant" >&2
    exit 1
  fi
  # A spec is a couple of megabytes; anything tiny means we saved an error page.
  if ! grep -q 'Checkmk REST-API' "$target"; then
    echo "What we saved does not look like a specification: ${target}" >&2
    exit 1
  fi
  printf '  %-40s %8s\n' "${target##*/}" "$(du -h "$target" | cut -f1)"
done

# Record which build a spec came from, as the file name only carries X.Y.Z.
provenance="${output_dir}/openapi-${version}.provenance"
{
  echo "build: ${build}"
  echo "variants: ${variants// /, }"
  echo "endpoint: ${api_url}/openapi-<variant>.yaml"
} > "$provenance"
printf '  %-40s %8s\n' "${provenance##*/}" "$(du -h "$provenance" | cut -f1)"
