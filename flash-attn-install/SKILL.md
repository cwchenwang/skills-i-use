---
name: flash-attn-install
description: Install flash-attention from prebuilt wheels at mjun0812/flash-attention-prebuild-wheels, matched to the current torch/python/cuda/arch. Use when the user asks to install flash-attention, flash-attn, or is fighting a flash-attn source build. Scans every release (paginated), picks the latest matching wheel, pip installs with --no-deps, records the install, and runs an import smoke test.
---

# flash-attn-install

Skip the source build. Find a wheel from `mjun0812/flash-attention-prebuild-wheels` that matches the target Python env, install it, log what was installed, and verify the import works.

## When to invoke

- User says "install flash attention" / "install flash-attn" / "I need flash attn"
- User is on a slow / failing source build (`pip install flash-attn` hanging on `ninja`)
- User wants a wheel for a specific torch+cuda combo (e.g. matching their training container)

## How it works

`find_wheel.py` does the search-and-install:

1. **Detect** torch, python, cuda, arch from the active Python interpreter:
   - torch: `torch.__version__` → major.minor
   - cuda: `torch.version.cuda` → encoded as `cuMMm` (e.g. `12.6` → `126`)
   - python: `sys.version_info` → `cpXY`
   - arch: `platform.machine()` → `x86_64` or `aarch64`
2. **Paginate** the GitHub releases API (`per_page=100`).
3. **Filter** assets matching all four tokens. `abi3` wheels match any `cp >= tag`.
4. **Rank** by latest flash-attn version (prefer `manylinux_*` over plain `linux_*` as a mild tiebreaker).
5. With `--install`: pip install `--no-deps`, then smoke-test `import flash_attn` (or `flash_attn_3`).
6. **Record** every install in `installs.jsonl` next to the script.

## Usage

Run with the **target environment's** Python — NOT the system Python — because torch/cuda are read from the running interpreter:

```bash
# Inside the target env (conda/venv activated, or full interpreter path):
TARGET_PY=/path/to/env/bin/python

# 1. Find best wheel (no install):
$TARGET_PY ~/.claude/skills/flash-attn-install/find_wheel.py

# 2. List every match across releases:
$TARGET_PY ~/.claude/skills/flash-attn-install/find_wheel.py --all

# 3. Install + smoke test:
$TARGET_PY ~/.claude/skills/flash-attn-install/find_wheel.py --install

# 4. Override versions (e.g. probing what's available without torch installed):
$TARGET_PY ~/.claude/skills/flash-attn-install/find_wheel.py --torch 2.5 --cuda 12.6 --python 3.10 --arch x86_64

# 5. FA3 (Hopper/Blackwell) instead of FA2:
$TARGET_PY ~/.claude/skills/flash-attn-install/find_wheel.py --fa-version 3 --install

# 6. Dry-run to see the pip command without running it:
$TARGET_PY ~/.claude/skills/flash-attn-install/find_wheel.py --install --dry-run
```

## What the agent should do when invoked

1. **Identify the target env.** Don't blindly use `python3` on PATH — that's usually system Python without torch. Look for `conda activate <name>`, a `venv/bin/python`, the user's container's interpreter, or ask if unclear.
2. **Dry-run first.** Show the matched wheel URL and the pip command before installing. Confirm flash-attn major version (FA2 vs FA3) — on Hopper/Blackwell, FA3 is faster.
3. **Cluster caveat — don't pip install on a busy login node.** Wheels are ~150-400 MB. On Slurm clusters, run on a compute node or use `cpu_datamover` for the download:
   ```bash
   srun --account=<acct> --partition=cpu_datamover --cpus-per-task=8 --time=0:30:00 \
       $TARGET_PY ~/.claude/skills/flash-attn-install/find_wheel.py --install
   ```
4. **Inspect the record after install** — `installs.jsonl` shows what got installed where and whether the smoke test passed.
5. **If no match**, surface the searched tokens to the user. Ask if they can bump torch (the repo tracks recent torch versions better than older ones) or check the repo for new releases:
   `https://github.com/mjun0812/flash-attention-prebuild-wheels/releases`

## Records

After `--install`, the script appends a JSON line to `~/.claude/skills/flash-attn-install/installs.jsonl`:

```json
{"release_tag": "v0.9.20", "wheel": "flash_attn-2.8.3+cu130torch2.11-cp313-cp313-linux_aarch64.whl",
 "url": "https://github.com/...", "flash_attn_version": "2.8.3", "pkg": "flash_attn",
 "env": {"py": "313", "torch": "2.11", "cuda": "130", "arch": "aarch64",
         "interpreter": "/path/to/env/bin/python"},
 "pip_rc": 0, "smoke_test_ok": true, "smoke_test_output": "flash_attn imported OK, version= 2.8.3",
 "timestamp": "2026-05-23T..."}
```

Use this to answer "what flash-attn did I install in this env?" without re-running anything.

## Caveats

- **Community-built wheels.** Verify SHAs at the release page if you're security-conscious.
- **`--no-deps`** is intentional — flash-attn depends on torch but we don't want pip re-resolving the user's pinned torch.
- **GitHub rate limit**: 60 unauth req/hour. Set `GITHUB_TOKEN` env var (any PAT, no scopes) if hit.
- **The wheel naming convention may evolve.** The regex in `find_wheel.py` covers `flash_attn{_3}-VER+cuNNNtorchM.m[gitSHA]-cpXY-{cpXY|abi3}-{arch}.whl` as of 2026-05. If the upstream repo changes naming, update `WHEEL_RE` there.
- **FA3 is `flash_attn_3`** as the import name — the script picks the right import target for the smoke test.

## Source

- Wheels: https://github.com/mjun0812/flash-attention-prebuild-wheels/releases
- Script: `~/.claude/skills/flash-attn-install/find_wheel.py`
- Records: `~/.claude/skills/flash-attn-install/installs.jsonl`
