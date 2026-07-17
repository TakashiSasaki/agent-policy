---
name: bootstrap-agent-policy
description: Initialize an unmanaged Git repository with the shared TakashiSasaki/agent-policy system by invoking a pinned main-branch toolchain revision, first in dry-run mode and then, only when requested, in apply mode.
---

# Bootstrap agent policy

Use this skill when a Git repository does not contain `.agent-policy.yml` and the user asks to adopt the shared agent-policy system.

## Procedure

1. Locate the target Git repository root.
2. Inspect whether `.agent-policy.yml`, `AGENTS.md`, `policy/project.md`, or agent-policy generated skills already exist.
3. Run `python scripts/bootstrap.py --repository <root>` without `--apply`.
4. Review the proposed files and any conflicts. Do not bypass a handwritten-file conflict.
5. Run with `--apply` only when repository initialization was requested.
6. After application, require both `agent-policy validate` and `agent-policy check` to succeed.
7. Report the pinned toolchain revision, created files, validation result, and any unresolved state.

## Safety constraints

- Execute only the full commit SHA in `bootstrap-manifest.yml`; never replace it with `main`, a tag, or another mutable reference.
- Do not commit, push, create branches, or modify GitHub settings unless separately requested.
- Do not overwrite existing non-generated agent instructions.
- Treat bootstrap-script or manifest updates as trust-anchor changes requiring explicit review.
