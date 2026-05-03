# Contributing to xrtm Governance

`governance` is the source of truth for XRTM-wide schemas, compatibility rules, release discipline, and contributor/review policy. Change this repo when you are changing a standard or shared operating rule, not when you are only implementing package behavior.

## Start with the right repo

| If you are changing... | Start here | Why |
| --- | --- | --- |
| Forecast Object schemas, compatibility policy, release discipline, triage, or contributor/review rules | `governance` | shared standards belong here |
| released CLI/product behavior or package-specific docs | [`xrtm`](https://github.com/xrtm-org/xrtm) or the owning package repo | implementation truth belongs with the code |
| runtime APIs, providers, or package examples | [`forecast`](https://github.com/xrtm-org/forecast) or the owning package repo | package behavior should not be defined here |
| public site navigation or repo-map presentation | [`xrtm.org`](https://github.com/xrtm-org/xrtm.org) | the site mirrors accepted policy/product truth |

## Local setup

Most policy/doc edits do not need a heavy environment. For schema validation, use `uvx` so contributors do not have to pre-install extra tooling globally.

## Standard checks

Validate committed JSON files with the same checker CI uses:

```bash
find . -name '*.json' -not -path './.*' -exec uvx --from check-jsonschema check-jsonschema --check-metaschema {} +
```

If your change updates a policy or schema consumed by another repo, also validate the affected downstream repo(s) before opening the PR.

## What belongs here

- **`schemas/`**: organization-wide contracts and compatibility guidance.
- **`policies/`**: PR acceptance, release readiness, cross-repo coordination, feature status, and triage rules.
- **`README.md`, `MISSION.md`, `ARCHITECTURE.md`**: shared philosophy and ecosystem structure.

Not here: package API docs, repo-local implementation tests, or newcomer site navigation.

## PR expectations

1. Preserve backward compatibility for published schemas, or document the migration path explicitly.
2. Record which downstream repos or release-pinned docs are affected.
3. Mirror accepted governance changes into repo-local docs/templates only where they materially reduce contributor ambiguity.
4. Include the validation command(s) you ran in the PR description.
