#!/usr/bin/env bash
# Send a push notification to the user's ntfy topic (phone/laptop).
# Reads NTFY_TOPIC / NTFY_SERVER from ~/.config/notify/env (shared with the
# slurm-notify skill), so there's a single place to configure the destination.
#
# Usage:
#   ntfy-send [-t TITLE] [-p PRIORITY] [-T TAGS] [-c CLICK_URL] MESSAGE...
#
#   -t  title (notification headline)
#   -p  priority: max|high|default|low|min          (default: default)
#   -T  comma-separated tags/emojis, e.g. white_check_mark,rocket
#   -c  click URL (opened when the notification is tapped)
#
# Examples:
#   ntfy-send "training finished"
#   ntfy-send -t "Job 12345" -p high -T warning "FAILED on node nvl-07"
#   ntfy-send -t "Done" -T white_check_mark -c "http://localhost:8042/" "viewer ready"
set -euo pipefail

[ -f "$HOME/.config/notify/env" ] && . "$HOME/.config/notify/env"

TITLE="" ; PRIO="default" ; TAGS="" ; CLICK=""
while getopts "t:p:T:c:h" opt; do
  case "$opt" in
    t) TITLE=$OPTARG ;;
    p) PRIO=$OPTARG ;;
    T) TAGS=$OPTARG ;;
    c) CLICK=$OPTARG ;;
    h) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "see: ntfy-send -h" >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))

MSG="$*"
[ -n "$MSG" ] || { echo "ntfy-send: empty message (see -h)" >&2; exit 2; }
: "${NTFY_TOPIC:?NTFY_TOPIC not set — add it to ~/.config/notify/env (see the ntfy-push skill)}"

HDRS=(-H "Priority: ${PRIO}")
[ -n "$TITLE" ] && HDRS+=(-H "Title: ${TITLE}")
[ -n "$TAGS"  ] && HDRS+=(-H "Tags: ${TAGS}")
[ -n "$CLICK" ] && HDRS+=(-H "Click: ${CLICK}")

code=$(curl -fsS -m 10 -o /dev/null -w '%{http_code}' \
  "${HDRS[@]}" -d "$MSG" "${NTFY_SERVER:-https://ntfy.sh}/${NTFY_TOPIC}") || {
    echo "ntfy-send: push failed (network/HTTP error)" >&2; exit 1; }
echo "ntfy-send: pushed to ${NTFY_SERVER:-https://ntfy.sh}/${NTFY_TOPIC} (HTTP ${code})"
