#!/usr/bin/env bash
#
# Written by: Robin Gierse - robin.gierse@checkmk.com - on 20260727
#
# Purpose:
# Manage GitHub Actions workflow runs for this repository.
#
# Usage:
#   Show the state of the latest runs:    ./gh.sh -m status
#   Show the state of runs for a branch:  ./gh.sh -m status -b fix/improve-api-reliability
#   Show only runs in a certain state:    ./gh.sh -m status -s failure
#   Show runs in one of several states:   ./gh.sh -m status -s failure,cancelled,in_progress
#   Rerun failed runs for a commit:       ./gh.sh -m rerun_failed -c 19199af1aec874f0003b0631e0621b67a99aec60
#   Rerun failed runs for a branch:       ./gh.sh -m rerun_failed -b fix/improve-api-reliability
#   Cancel queued runs for a branch:      ./gh.sh -m cancel_queued -b fix/improve-api-reliability
#   Delete completed runs for a commit:   ./gh.sh -m delete_completed -c <sha>
#   Any of the above with a custom limit: ./gh.sh -m rerun_failed -c <sha> -l 100

limit=1000
status_limit=30
states=()
valid_states="action_required cancelled completed failure in_progress neutral pending queued requested skipped stale startup_failure success timed_out waiting"

while getopts 'm:c:b:l:s:' OPTION; do
  case "$OPTION" in
    m)
      mode="$OPTARG" ;;
    c)
      commit="$OPTARG" ;;
    b)
      branch="$OPTARG" ;;
    l)
      limit="$OPTARG"
      status_limit="$OPTARG" ;;
    s)
      state="$OPTARG" ;;
    ?)
      echo "Unknown option!"
      exit 1
      ;;
  esac
done

if [ -n "${state}" ]; then
  if [ "${mode}" != "status" ]; then
    echo "The state filter (-s) is only supported in status mode!"
    exit 1
  fi
  IFS=',' read -r -a states <<< "${state}"
  for wanted_state in "${states[@]}"; do
    case " ${valid_states} " in
      *" ${wanted_state} "*)
        ;;
      *)
        echo "Unknown state <${wanted_state}>!"
        echo "Valid states are: ${valid_states// /, }"
        exit 1
        ;;
    esac
  done
fi

if [ -n "${commit}" ]; then
  filter_args=(-c "${commit}")
  target="commit <${commit}>"
elif [ -n "${branch}" ]; then
  filter_args=(-b "${branch}")
  target="branch <${branch}>"
elif [ "${mode}" = "status" ]; then
  filter_args=()
  target="this repository"
else
  echo "Please provide either a commit sha with -c or a branch with -b!"
  exit 1
fi

_run_status() {
    json_fields="databaseId,status,conclusion,workflowName,headBranch,event,startedAt"

    if [ "${#states[@]}" -eq 0 ]; then
        echo "## Showing the ${status_limit} most recent workflow runs for ${target}."
        runs="$(gh run list "${filter_args[@]}" --limit "${status_limit}" --json "${json_fields}")"
    else
        echo "## Showing the ${status_limit} most recent workflow runs per state for ${target}."
        echo "## Filtering for state(s): ${states[*]}"
        # One query per state, since 'gh run list --status' accepts a single value only.
        runs="$(for wanted_state in "${states[@]}"; do
                    gh run list "${filter_args[@]}" --limit "${status_limit}" \
                        --status "${wanted_state}" --json "${json_fields}"
                done | jq -s 'add | unique_by(.databaseId) | sort_by(.startedAt) | reverse')"
    fi

    if [ -z "${runs}" ] || [ "${runs}" = "[]" ] || [ "${runs}" = "null" ]; then
        echo "No workflow runs found."
        return 0
    fi

    jq_helpers='
        def age($t):
            if $t == null or $t == "" then "-" else
            (now - ($t | fromdateiso8601)) as $s
            | if   $s <    60 then "\($s          | floor)s"
              elif $s <  3600 then "\($s /    60  | floor)m"
              elif $s < 86400 then "\($s /  3600  | floor)h"
              else                 "\($s / 86400  | floor)d" end end;
        def state: if .conclusion == "" or .conclusion == null then .status else .conclusion end;
        def glyph:
            if   .status != "completed" then "*"
            elif .conclusion == "success"   then "+"
            elif .conclusion == "failure"   then "!"
            elif .conclusion == "cancelled" then "-"
            elif .conclusion == "skipped"   then "~"
            else "?" end;
    '

    printf '%s' "${runs}" | jq -r "${jq_helpers}"'
        (["", "STATE", "WORKFLOW", "BRANCH", "EVENT", "AGE", "ID"]),
        (.[] | [glyph, state, .workflowName, .headBranch, .event, age(.startedAt), (.databaseId | tostring)])
        | @tsv' | column -t -s "$(printf '\t')"

    echo
    printf '%s' "${runs}" | jq -r "${jq_helpers}"'
        group_by(state) | map("\(.[0] | state): \(length)") | join("  |  ")
        | "## Summary: " + .'
}

_run_rerun_failed() {
    echo "## Rerunning failed workflow runs for ${target}."
    for id in $(gh run list "${filter_args[@]}" --status failure --limit "${limit}" --json databaseId --jq '.[].databaseId'); do
        gh run rerun "$id" --failed
    done
    echo "## Rerun done."
}

_run_cancel_queued() {
    echo "## Cancelling queued workflow runs for ${target}."
    for id in $(gh run list "${filter_args[@]}" --limit "${limit}" --json databaseId,status --jq '.[] | select(.status == "queued") | .databaseId'); do
        gh run cancel "$id"
    done
    echo "## Cancel done."
}

_run_delete_completed() {
    echo "## Deleting completed workflow runs for ${target}."
    for id in $(gh run list "${filter_args[@]}" --limit "${limit}" --json databaseId,status --jq '.[] | select(.status == "completed") | .databaseId'); do
        gh run delete "$id"
    done
    echo "## Delete done."
}

case "$mode" in
    status)
        _run_status ;;
    rerun_failed)
        _run_rerun_failed ;;
    cancel_queued)
        _run_cancel_queued ;;
    delete_completed)
        _run_delete_completed ;;
    *)
        echo "Please choose a mode with -m: status, rerun_failed, cancel_queued or delete_completed."
        exit 1
        ;;
esac
