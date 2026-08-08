---
name: bootstrap-agent-policy
description: Deprecated historical bootstrap. Do not use this branch for new adoption; use the integrated bootstrap skill from TakashiSasaki/templates policy instead.
---

# Bootstrap agent policy

> [!WARNING]
> This bootstrap branch is deprecated and retained only so historical full-SHA references remain addressable. For new adoption, use the integrated `bootstrap-agent-policy` skill from `TakashiSasaki/templates` branch `policy` and its reviewed stable full-SHA release. The stable toolchain revision at deprecation time is `5de32547e68fa15e24ff3b8affadf12e9d730a41`.

The procedure below documents the historical behavior of this branch and is preserved for old pinned references. Do not start new adoption from the mutable branch tip.

Use this skill when a Git repository does not contain `.agent-policy.yml` and the user asks to adopt the shared `TakashiSasaki/agent-policy` system.

## Procedure

1. Locate the target Git repository root.
2. Run `python scripts/bootstrap.py --repository <root>` without `--apply`.
3. Review the reported repository state, discovered instruction sources, recommended route, and the dry-run plan from the pinned toolchain.
4. For `unmanaged-empty`, apply initialization only after an explicit request:
   `python scripts/bootstrap.py --repository <root> --route init --apply`.
5. For `unmanaged-existing`, select one discovered instruction file as the primary source and review adoption preparation:
   `python scripts/bootstrap.py --repository <root> --route adopt --primary-instructions <path>`.
6. Apply adoption preparation only after an explicit request by adding `--apply`. This creates the adoption state and generated preview, then runs `agent-policy adopt preview`; it does not replace the primary instructions.
7. Help move repository-specific semantic requirements into the project policy and review the generated preview. Do not silently translate or discard handwritten requirements.
8. Run `agent-policy adopt finalize --apply` from the same pinned toolchain only after a separate explicit instruction to finalize the reviewed adoption.
9. Require `agent-policy validate` and `agent-policy check` to succeed after initialization or completed finalization. Report the pinned toolchain revision, selected route, affected files, and unresolved state.

## Safety constraints

- Execute only the full commit SHA in `bootstrap-manifest.yml`; never replace it with `main`, a tag, a short SHA, or another mutable reference.
- Treat automatic route selection as dry-run advice only. Any mutation requires explicit `--route init` or `--route adopt`.
- `scripts/bootstrap.py` may apply initialization or adoption preparation only. It must never invoke adoption finalization.
- Do not bypass a handwritten-file conflict or an inconsistent repository state.
- Do not commit, push, create branches, or modify GitHub settings unless separately requested.
- Do not overwrite, delete, or semantically reinterpret existing non-generated agent instructions without explicit review.
- Treat bootstrap-script, manifest, route, or safety-constraint updates as trust-anchor changes requiring explicit review.
