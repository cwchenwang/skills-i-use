#!/usr/bin/env python3
"""Find and optionally install a flash-attention wheel from
mjun0812/flash-attention-prebuild-wheels matching the current env.

Auto-detects torch, python, cuda, arch — override with --torch / --cuda /
--python / --arch. Scans every release (paginated), filters assets by tokens,
picks the latest flash-attn version among matches.
"""

import argparse
import datetime
import json
import os
import pathlib
import platform
import re
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Optional

REPO_API = "https://api.github.com/repos/mjun0812/flash-attention-prebuild-wheels/releases"
RECORD_PATH = pathlib.Path(__file__).resolve().parent / "installs.jsonl"

# Examples seen:
#   flash_attn-2.8.3+cu130torch2.11-cp313-cp313-linux_aarch64.whl
#   flash_attn_3-3.0.0+cu126torch2.12gite2743ab-cp39-abi3-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl
WHEEL_RE = re.compile(
    r"^(?P<pkg>flash_attn(?:_3)?)-"
    r"(?P<flash>\d+(?:\.\d+)*(?:\.post\d+)?)\+"
    r"cu(?P<cuda>\d+)"
    r"torch(?P<torch>\d+\.\d+)"
    r"(?:git[0-9a-f]+)?-"
    r"cp(?P<py>\d+)-"
    r"(?P<abi>cp\d+|abi3)-"
    r"(?P<plat>.+)\.whl$"
)


def detect_env() -> dict:
    py = f"{sys.version_info.major}{sys.version_info.minor}"
    arch = "aarch64" if platform.machine() in ("aarch64", "arm64") else "x86_64"
    torch_v, cuda_v = None, None
    try:
        import torch  # type: ignore
        torch_v = ".".join(torch.__version__.split("+")[0].split(".")[:2])
        if torch.version.cuda:
            maj, mn = torch.version.cuda.split(".")[:2]
            cuda_v = f"{int(maj)}{int(mn)}"
    except Exception:
        # Fall back to pip metadata — works on login nodes without CUDA libs.
        try:
            import importlib.metadata as md
            raw = md.version("torch")  # e.g. "2.11.0+cu128"
            torch_v = ".".join(raw.split("+")[0].split(".")[:2])
            if "+cu" in raw:
                cuda_v = raw.split("+cu", 1)[1].split(".", 1)[0]
        except Exception:
            pass
    return {"py": py, "torch": torch_v, "cuda": cuda_v, "arch": arch}


def list_releases(token: Optional[str] = None):
    page = 1
    while True:
        url = f"{REPO_API}?per_page=100&page={page}"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github+json")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                batch = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 403 and "rate limit" in (e.read() or b"").decode("utf8", "ignore").lower():
                raise SystemExit(
                    "GitHub API rate limit hit. Set GITHUB_TOKEN env var "
                    "(any personal access token, no scopes needed)."
                )
            raise
        if not batch:
            return
        yield from batch
        if len(batch) < 100:
            return
        page += 1


def _parse_ver(s: str):
    return tuple(int(x) for x in re.findall(r"\d+", s))


def find_matches(env: dict, fa_major: str = "2", token: Optional[str] = None):
    want_pkg = "flash_attn_3" if fa_major.startswith("3") else "flash_attn"
    out = []
    for rel in list_releases(token):
        for asset in rel.get("assets", []):
            m = WHEEL_RE.match(asset["name"])
            if not m:
                continue
            g = m.groupdict()
            if g["pkg"] != want_pkg:
                continue
            if env["torch"] and g["torch"] != env["torch"]:
                continue
            if env["cuda"] and g["cuda"] != env["cuda"]:
                continue
            if g["abi"] == "abi3":
                if int(env["py"]) < int(g["py"]):
                    continue
            else:
                if g["py"] != env["py"]:
                    continue
            if env["arch"] not in g["plat"]:
                continue
            out.append((rel["tag_name"], asset, g))
    return out


def smoke_test(pkg: str) -> tuple[bool, str]:
    """Import the package in a subprocess (same interpreter) and return (ok, output)."""
    code = (
        f"import {pkg}; "
        f"v = getattr({pkg}, '__version__', '?'); "
        f"print({pkg!r}, 'imported OK, version=', v)"
    )
    try:
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=30,
        )
        out = (r.stdout + r.stderr).strip()
        return r.returncode == 0, out
    except subprocess.TimeoutExpired:
        return False, "smoke test timed out after 30s"


def record_install(entry: dict) -> None:
    """Append-only JSON-lines log of installs."""
    entry["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with RECORD_PATH.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        print(f"warn: failed to write record {RECORD_PATH}: {e}", file=sys.stderr)


def pick_best(matches):
    def key(item):
        _tag, _asset, g = item
        manylinux = 1 if "manylinux" in g["plat"] else 0
        return (_parse_ver(g["flash"]), manylinux, _parse_ver(_tag))
    return max(matches, key=key)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--torch", help="Torch major.minor (e.g. 2.5). Auto if omitted.")
    ap.add_argument("--cuda", help="CUDA as M.m or MMm (e.g. 12.6 or 126). Auto if omitted.")
    ap.add_argument("--python", help="Python tag: 3.10 / 310 / cp310. Auto if omitted.")
    ap.add_argument("--arch", choices=["x86_64", "aarch64"], help="Auto if omitted.")
    ap.add_argument("--fa-version", default="2", choices=["2", "3"],
                    help="Flash-attn major: 2 or 3 (default 2).")
    ap.add_argument("--install", action="store_true",
                    help="pip install the matched wheel with --no-deps.")
    ap.add_argument("--all", action="store_true",
                    help="List every matching wheel (not just best).")
    ap.add_argument("--dry-run", action="store_true",
                    help="With --install: print pip command, don't run.")
    args = ap.parse_args()

    env = detect_env()
    if args.torch:
        v = args.torch.lstrip("v").split("+")[0]
        env["torch"] = ".".join(v.split(".")[:2])
    if args.cuda:
        c = args.cuda.replace(".", "")
        env["cuda"] = c
    if args.python:
        env["py"] = args.python.lower().removeprefix("cp").replace(".", "")
    if args.arch:
        env["arch"] = args.arch

    print(f"Searching: torch={env['torch']} cuda={env['cuda']} "
          f"py=cp{env['py']} arch={env['arch']} fa{args.fa_version}",
          file=sys.stderr)
    if not env["torch"] or not env["cuda"]:
        print("ERROR: torch/cuda not detected. Either activate an env with torch "
              "installed, or pass --torch and --cuda.", file=sys.stderr)
        return 2

    token = os.environ.get("GITHUB_TOKEN")
    matches = find_matches(env, fa_major=args.fa_version, token=token)
    if not matches:
        print("No matching wheel found across all releases.", file=sys.stderr)
        print("Try a different --torch/--cuda/--fa-version, or check repo for "
              "newer releases:", file=sys.stderr)
        print("  https://github.com/mjun0812/flash-attention-prebuild-wheels/releases",
              file=sys.stderr)
        return 1

    if args.all:
        for tag, asset, _g in matches:
            print(f"{tag}\t{asset['name']}\t{asset['browser_download_url']}")
        return 0

    tag, asset, g = pick_best(matches)
    print(f"Best match: release {tag}, flash-attn {g['flash']} ({asset['name']})",
          file=sys.stderr)
    print(asset["browser_download_url"])

    if args.install or args.dry_run:
        cmd = [sys.executable, "-m", "pip", "install", "--no-deps",
               asset["browser_download_url"]]
        print("pip command:", " ".join(cmd), file=sys.stderr)
        if args.dry_run:
            return 0
        rc = subprocess.call(cmd)
        ok, out = (False, "skipped — pip install failed") if rc != 0 else smoke_test(g["pkg"])
        record_install({
            "release_tag": tag,
            "wheel": asset["name"],
            "url": asset["browser_download_url"],
            "flash_attn_version": g["flash"],
            "pkg": g["pkg"],
            "env": {**env, "interpreter": sys.executable},
            "pip_rc": rc,
            "smoke_test_ok": ok,
            "smoke_test_output": out,
        })
        print(f"smoke test: {'PASS' if ok else 'FAIL'} — {out}", file=sys.stderr)
        print(f"record: {RECORD_PATH}", file=sys.stderr)
        return 0 if rc == 0 and ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
