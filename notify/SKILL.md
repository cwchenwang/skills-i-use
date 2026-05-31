---
name: notify
description: Push notifications to the user's phone/laptop via ntfy.sh. Two modes — (1) ad-hoc sends via the `ntfy-send` CLI ("ping me when X finishes", a one-off push from a script, or YOU the agent alerting the user that a long task you started has completed); (2) automatic Slurm/sbatch job-completion alerts via a one-line EXIT-trap (`notify.sh`). Use whenever the user wants to be notified, pinged, alerted, or texted when something finishes, succeeds, or fails. Manages the shared ~/.config/notify/env topic.
---

# notify

Push notifications to the user's devices through [ntfy.sh](https://ntfy.sh). One
topic, configured once in `~/.config/notify/env`; the user subscribes to it in the
ntfy app or at `https://ntfy.sh/<topic>`. No account or secret needed.

Bundled here:
- `ntfy-send.sh` → the `ntfy-send` CLI (symlinked onto PATH at `~/.local/bin/ntfy-send`).
- `notify.sh`    → an EXIT-trap notifier you `source` into sbatch scripts.

## Config (`~/.config/notify/env`, chmod 600)
```sh
export NTFY_TOPIC="<unguessable-topic>"     # required
# export NTFY_SERVER="https://ntfy.sh"      # optional: self-hosted server
```
If `NTFY_TOPIC` is missing, create one and tell the user to subscribe:
```sh
mkdir -p ~/.config/notify
echo "export NTFY_TOPIC=\"$USER-ntfy-$(head -c6 /dev/urandom | od -An -tx1 | tr -d ' \n')\"" >> ~/.config/notify/env
chmod 600 ~/.config/notify/env
```
Public ntfy.sh topics are readable by anyone who guesses the name — keep it random
and never put secrets in a message; use `NTFY_SERVER` (self-hosted) for anything sensitive.

## Mode 1 — ad-hoc push (`ntfy-send`)
```
ntfy-send [-t TITLE] [-p max|high|default|low|min] [-T TAGS] [-c CLICK_URL] MESSAGE...
```
Examples:
```sh
ntfy-send "training finished"
ntfy-send -t "Job 12345" -p high -T warning "FAILED on nvl-07 after 2h"
ntfy-send -t "Viewer ready" -T white_check_mark -c "http://localhost:8042/" "camera_viewer up"
```
"Ping me when X is done" → run the task, then push:
```sh
<long task> && ntfy-send -t "Done" -T white_check_mark "X finished OK" \
            || ntfy-send -t "Failed" -p high -T warning "X failed (rc=$?)"
```

## Mode 2 — automatic Slurm job-completion (`notify.sh` EXIT trap)
Add ONE line near the top of an sbatch, right after `set -euo pipefail`:
```sh
source "$HOME/.config/notify/notify.sh" 2>/dev/null || true
```
The trap fires at job exit (success AND failure), pushing `OK` / `FAILED rc=N` with
job name, id, host, and elapsed time. No-op if `NTFY_TOPIC` is unset. Reusable across
repos since it lives in `$HOME`.

## Notes
- Outbound HTTPS to ntfy.sh works from SIL cluster login/compute nodes (verified).
- The trap captures the real exit code first thing, so failures report `FAILED rc=N`.
- `sbatch --mail-type` does NOT work on SIL clusters (`MailDomain=null`); use this instead.
- (Slack delivery was intentionally dropped for now — ntfy only. Re-add a webhook channel later if needed.)
