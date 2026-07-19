# bootstrap-agent-policy

This orphan branch is a directly cloneable agent skill package for onboarding repositories to the `TakashiSasaki/agent-policy` system. Its Git history is unrelated to `main`.

`SKILL.md` is at the branch root so the checkout directory itself is the skill directory. The package contains only the trust seed and orchestration needed to invoke one immutable `main` revision; policy compilation and adoption transactions remain in the pinned toolchain.

## Direct clone

```bash
git clone \
  --branch bootstrap-agent-policy \
  --single-branch \
  https://github.com/TakashiSasaki/agent-policy.git \
  bootstrap-agent-policy
```

For a user-level skill directory, provide the complete destination path as the final clone argument.

## Submodule

```bash
git submodule add \
  -b bootstrap-agent-policy \
  https://github.com/TakashiSasaki/agent-policy.git \
  .agents/skills/bootstrap-agent-policy
```

A submodule records a specific commit. Do not configure unattended tracking of the branch tip for this trust seed.

## Repository inspection and dry run

Dry-run is the default. The script invokes the pinned `agent-policy adopt inspect`, reports the discovered state and sources, recommends `init` or `adopt`, and runs the selected route without applying changes.

```bash
python scripts/bootstrap.py --repository /path/to/product
```

The relevant states are:

- `unmanaged-empty`: use `init`;
- `unmanaged-existing`: use `adopt` preparation;
- `managed`: stop because bootstrap is no longer required;
- `inconsistent`: stop and repair or remove partial/generated artifacts explicitly.

Automatic route selection is advisory and available only for dry runs. Applying a route requires an explicit route selection.

## Apply initialization

```bash
python scripts/bootstrap.py \
  --repository /path/to/product \
  --route init \
  --apply
```

After initialization the script runs `agent-policy validate` and `agent-policy check` with the same pinned toolchain.

## Prepare adoption of existing instructions

First select one instruction file reported by inspection as the primary source:

```bash
python scripts/bootstrap.py \
  --repository /path/to/product \
  --route adopt \
  --primary-instructions AGENTS.md
```

Apply only after reviewing the preparation plan:

```bash
python scripts/bootstrap.py \
  --repository /path/to/product \
  --route adopt \
  --primary-instructions AGENTS.md \
  --apply
```

This applies `agent-policy adopt prepare` and then runs `agent-policy adopt preview`. It preserves the primary handwritten instructions and does not finalize the cutover. Finalization requires a separate explicit invocation of `agent-policy adopt finalize --apply` from the pinned toolchain after the project policy and preview have been reviewed.

## Trust boundary

`bootstrap-manifest.yml` pins a full `main` commit SHA and declares only inspection, initialization, adoption preparation/preview, validation, and check routes. It deliberately contains no finalization route. After successful initialization or completed adoption, the product repository's `.agent-policy.yml` and `.agent-policy.lock` become the normal trust and reproducibility records.
