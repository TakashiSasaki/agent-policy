#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest() -> dict[str, object]:
    path = skill_root() / "bootstrap-manifest.yml"
    value = json.loads(path.read_text(encoding="utf-8"))
    toolchain = value.get("toolchain")
    if not isinstance(toolchain, dict):
        raise ValueError("Manifest toolchain must be an object")
    revision = toolchain.get("revision")
    if not isinstance(revision, str) or not FULL_SHA.fullmatch(revision):
        raise ValueError("Manifest revision must be a full lowercase Git commit SHA")
    if toolchain.get("repository") != "TakashiSasaki/agent-policy":
        raise ValueError("Unexpected toolchain repository")
    return value


def repository_root(raw: Path) -> Path:
    path = raw.expanduser().resolve()
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        capture_output=True,
    )
    return Path(result.stdout.strip()).resolve()


def git_requirement(repository: str, revision: str) -> str:
    return f"git+https://github.com/{repository}.git@{revision}"


def run_with_uvx(requirement: str, arguments: list[str], cwd: Path) -> int:
    command = ["uvx", "--from", requirement, "agent-policy", *arguments]
    return subprocess.run(command, cwd=cwd).returncode


def run_with_temporary_venv(requirement: str, calls: list[list[str]], cwd: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="bootstrap-agent-policy-") as temporary:
        venv = Path(temporary) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        if sys.platform == "win32":
            python = venv / "Scripts" / "python.exe"
            executable = venv / "Scripts" / "agent-policy.exe"
        else:
            python = venv / "bin" / "python"
            executable = venv / "bin" / "agent-policy"
        subprocess.run(
            [str(python), "-m", "pip", "install", "--disable-pip-version-check", requirement],
            check=True,
        )
        for arguments in calls:
            result = subprocess.run([str(executable), *arguments], cwd=cwd)
            if result.returncode:
                return result.returncode
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap TakashiSasaki/agent-policy")
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true", help="Apply changes after the default dry-run")
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest()
        root = repository_root(args.repository)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"bootstrap error: {exc}", file=sys.stderr)
        return 2

    if (root / ".agent-policy.yml").exists():
        print("bootstrap error: repository is already initialized", file=sys.stderr)
        return 3

    toolchain = manifest["toolchain"]
    assert isinstance(toolchain, dict)
    repository = str(toolchain["repository"])
    revision = str(toolchain["revision"])
    requirement = git_requirement(repository, revision)
    init_arguments = [
        "--repository", str(root), "init",
        "--toolchain-revision", revision,
    ]
    if args.apply:
        init_arguments.append("--apply")

    print(f"Toolchain: {repository}@{revision}")
    print(f"Repository: {root}")
    print(f"Mode: {'apply' if args.apply else 'dry-run'}")

    if shutil.which("uvx"):
        code = run_with_uvx(requirement, init_arguments, root)
        if code or not args.apply:
            return code
        for command in ("validate", "check"):
            code = run_with_uvx(
                requirement,
                ["--repository", str(root), command, "--config", ".agent-policy.yml"],
                root,
            )
            if code:
                return code
        return 0

    calls = [init_arguments]
    if args.apply:
        calls.extend([
            ["--repository", str(root), "validate", "--config", ".agent-policy.yml"],
            ["--repository", str(root), "check", "--config", ".agent-policy.yml"],
        ])
    try:
        return run_with_temporary_venv(requirement, calls, root)
    except subprocess.CalledProcessError as exc:
        print(f"bootstrap error: command failed with status {exc.returncode}", file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
