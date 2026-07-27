#!/usr/bin/env bash
#
# Written by: Robin Gierse - robin.gierse@checkmk.com - on 20260727
#
# Purpose:
# Manage GitHub Actions workflow runs for this repository.
#
# Usage:
#   Rerun failed runs for a commit:       ./gh.sh -m rerun_failed -c 19199af1aec874f0003b0631e0621b67a99aec60
#   Rerun failed runs for a branch:       ./gh.sh -m rerun_failed -b fix/improve-api-reliability
#   Cancel queued runs for a branch:      ./gh.sh -m cancel_queued -b fix/improve-api-reliability
#   Delete completed runs for a commit:   ./gh.sh -m delete_completed -c <sha>
#   Any of the above with a custom limit: ./gh.sh -m rerun_failed -c <sha> -l 100

limit=5000

while getopts 'm:c:b:l:' OPTION; do
  case "$OPTION" in
    m)
      mode="$OPTARG" ;;
    c)
      commit="$OPTARG" ;;
    b)
      branch="$OPTARG" ;;
    l)
      limit="$OPTARG" ;;
    ?)
      echo "Unknown option!"
      exit 1
      ;;
  esac
done

if [ -n "${commit}" ]; then
  filter_args=(-c "${commit}")
  target="commit <${commit}>"
elif [ -n "${branch}" ]; then
  filter_args=(-b "${branch}")
  target="branch <${branch}>"
else
  echo "Please provide either a commit sha with -c or a branch with -b!"
  exit 1
fi

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
    rerun_failed)
        _run_rerun_failed ;;
    cancel_queued)
        _run_cancel_queued ;;
    delete_completed)
        _run_delete_completed ;;
    *)
        echo "Please choose a mode with -m: rerun_failed, cancel_queued or delete_completed."
        exit 1
        ;;
esac
