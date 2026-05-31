#!/usr/bin/env bash
# Slurm/job-finish notifier via ntfy push.
#
# Use: add ONE line near the top of any sbatch, after `set -euo pipefail`:
#     source "$HOME/.config/notify/notify.sh" 2>/dev/null || true
#
# Reads NTFY_TOPIC / NTFY_SERVER from $HOME/.config/notify/env (chmod 600).
# No-op if NTFY_TOPIC is unset. Fires on BOTH success and failure (EXIT trap),
# reporting the real exit code, elapsed time, job name/id, and host. The network
# call is best-effort and time-limited, so it never fails your job.

_NOTIFY_ENV="${NOTIFY_ENV:-$HOME/.config/notify/env}"
[ -f "$_NOTIFY_ENV" ] && . "$_NOTIFY_ENV"

_notify_send() {
    local rc=$?
    [ -n "${NTFY_TOPIC:-}" ] || return "$rc"
    local state tags prio
    if [ "$rc" -eq 0 ]; then state=OK; tags=white_check_mark; prio=default
    else state=FAILED; tags=warning; prio=high; fi
    local msg
    msg="$(printf "[%s] %s id=%s rc=%s host=%s elapsed=%dm %s" \
        "$state" "${SLURM_JOB_NAME:-job}" "${SLURM_JOB_ID:-local}" "$rc" \
        "$(hostname -s)" "$(( SECONDS / 60 ))" "$(date -Is)")"
    curl -fsS -m 10 \
        -H "Title: Job ${state}: ${SLURM_JOB_NAME:-job}" \
        -H "Priority: ${prio}" -H "Tags: ${tags}" \
        -d "$msg" "${NTFY_SERVER:-https://ntfy.sh}/${NTFY_TOPIC}" >/dev/null 2>&1 || true
    return "$rc"
}

trap _notify_send EXIT
