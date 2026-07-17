# bootstrap-agent-policy

This orphan branch is a directly cloneable agent skill package for initializing repositories with the `TakashiSasaki/agent-policy` system. Its Git history is unrelated to `main`.

`SKILL.md` is at the branch root so the checkout directory itself is the skill directory.

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

## Execution

Dry-run is the default:

```bash
python scripts/bootstrap.py --repository /path/to/product
```

Apply initialization:

```bash
python scripts/bootstrap.py --repository /path/to/product --apply
```

The manifest pins a full commit SHA from `main`. After successful initialization, the product repository's `.agent-policy.yml` and `.agent-policy.lock` become the normal trust and reproducibility records.
