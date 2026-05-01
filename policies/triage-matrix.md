# Triage Matrix

This matrix provides a structured decision framework for categorizing pull requests and issues during triage. Use this together with the [PR Acceptance Policy](pr-acceptance-policy.md) to ensure consistent, reproducible decisions.

## PR Triage Dimensions

Evaluate each pull request along these dimensions before recording a disposition:

### 1. Scope Classification

| Category | Definition | Examples |
| --- | --- | --- |
| **Core Schema** | Changes to `governance/schemas/` or `policies/` that affect interoperability | Forecast Object fields, compatibility rules |
| **Package API** | Public interfaces in `xrtm-data`, `xrtm-eval`, `xrtm-forecast`, `xrtm-train` | Exported functions, CLI arguments, configuration |
| **Implementation** | Internal logic without public API changes | Refactoring, optimization, bug fixes |
| **Infrastructure** | CI, build, packaging, deployment tooling | GitHub workflows, `pyproject.toml`, release scripts |
| **Documentation** | README, docstrings, guides, examples | Installation steps, API reference, tutorials |

### 2. Urgency Assessment

| Priority | Criteria |
| --- | --- |
| **Release Blocker** | Fixes a critical bug, unblocks dependent work, or prevents release |
| **High** | Valuable improvement with clear benefit; should target next planned release |
| **Medium** | Useful but not time-sensitive; can wait for appropriate release cycle |
| **Low** | Nice-to-have; defer unless bundled with related work |

### 3. Risk Level

| Risk | Indicators |
| --- | --- |
| **High** | Breaking changes, schema modifications, security fixes, large refactors |
| **Medium** | New features, provider changes, test coverage improvements |
| **Low** | Documentation, formatting, comment updates, isolated bug fixes |

### 4. Compatibility Impact

| Impact | Description |
| --- | --- |
| **Breaking** | Requires migration, removes public APIs, changes schema semantics |
| **Additive** | Adds optional features, extends schemas with backward compatibility |
| **Neutral** | Internal changes with no external impact |

## Issue Triage Dimensions

For issue reports, evaluate these factors:

### 1. Issue Type

| Type | Use when |
| --- | --- |
| **Bug** | Incorrect behavior, errors, crashes, or regression from documented/expected behavior |
| **Feature Request** | New capability, enhancement, or extension to existing functionality |
| **Question** | Usage help, clarification, or understanding existing behavior |
| **Maintenance** | Technical debt, refactoring, dependency updates, infrastructure improvements |

### 2. Severity (Bugs Only)

| Severity | Criteria |
| --- | --- |
| **Critical** | Data corruption, zero-leakage violation, security issue, or complete functionality failure |
| **High** | Major feature broken, incorrect results, or significant usability problem |
| **Medium** | Feature partially broken, edge case failure, or degraded performance |
| **Low** | Minor inconvenience, cosmetic issue, or rare edge case |

### 3. Reproducibility (Bugs Only)

| Status | Description |
| --- | --- |
| **Confirmed** | Reproduced locally with clear steps |
| **Reported** | Described with evidence but not yet reproduced |
| **Unclear** | Insufficient information to reproduce |

## Triage Decision Flow

Use this flow during triage sessions:

1. **Group related items**: Identify overlapping PRs, duplicate issues, or issue-PR pairs.
2. **Classify scope and type**: Use the dimension tables above.
3. **Assess priority and risk**: Determine urgency and compatibility impact.
4. **Apply decision criteria**: Use the [PR Acceptance Policy](pr-acceptance-policy.md) to select a disposition.
5. **Record in tracker**: Log the decision in `policies/pr-disposition-log.md` with evidence.
6. **Update PR/issue**: Add triage label and brief comment explaining the decision.

## Triage Labels

Use these labels across XRTM repositories for consistent filtering:

### PR Disposition Labels
- `disposition:accept` - Will merge as-is or with minor fixes
- `disposition:supersede` - Addressed by alternative implementation
- `disposition:defer` - Valid but not current priority
- `disposition:reject` - Not aligned with project goals or standards

### Issue Priority Labels
- `priority:blocker` - Blocks release or critical functionality
- `priority:high` - Important for next release
- `priority:medium` - Useful improvement
- `priority:low` - Nice-to-have

### Scope Labels
- `scope:schema` - Affects Forecast Object or compatibility
- `scope:api` - Changes public package interfaces
- `scope:docs` - Documentation only
- `scope:infra` - Build, CI, or tooling

### Type Labels
- `type:bug` - Incorrect behavior
- `type:feature` - New capability
- `type:maintenance` - Technical debt or refactoring

## Batch Triage Workflow

For periodic triage sessions:

1. **Prepare**: Pull latest changes, review `pr-acceptance-policy.md` and `release-readiness-policy.md`.
2. **Filter open items**: List all open PRs and issues, grouped by repository.
3. **Classify each item**: Apply scope, type, priority, and risk dimensions.
4. **Decide disposition**: Use acceptance criteria and decision categories.
5. **Record decisions**: Update `pr-disposition-log.md` with timestamp and rationale.
6. **Communicate**: Comment on PRs/issues with clear next steps.
7. **Track follow-up**: Ensure deferred or superseded items have tracking issues if needed.

## Escalation

If triage decisions are unclear:

- **Schema changes**: Consult governance maintainers before accepting.
- **Breaking API changes**: Require explicit compatibility plan and migration guide.
- **Security issues**: Triage privately, coordinate disclosure, prioritize fix.
- **Controversial features**: Seek consensus from multiple maintainers before accepting or rejecting.
