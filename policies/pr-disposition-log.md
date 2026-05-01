# PR Disposition Log

This log records triage decisions for pull requests across the XRTM organization. Maintain this log to ensure decision transparency, avoid re-litigating closed PRs, and track patterns in contribution quality.

## Purpose

- **Historical Record**: Track why PRs were accepted, modified, superseded, rejected, or deferred.
- **Pattern Recognition**: Identify common issues, frequent contributors, and areas needing documentation.
- **Decision Transparency**: Provide clear rationale for external contributors and future maintainers.

## Log Format

Each entry should include:

```
### [Repository#PR] Title (YYYY-MM-DD)

**Disposition**: [Accept as-is | Accept with changes | Supersede | Reject | Defer]
**Scope**: [Core Schema | Package API | Implementation | Infrastructure | Documentation]
**Priority**: [Release Blocker | High | Medium | Low]
**Risk**: [High | Medium | Low]

**Rationale**:
Brief explanation of why this disposition was chosen.

**Evidence**:
- Test results, code review findings, or validation gate outcomes
- Link to related issues, PRs, or discussion threads
- Superseding commit/PR if applicable

**Action Taken**:
- Merged as SHA: <commit-hash> (if accepted)
- Superseded by PR#XYZ or local commit SHA (if superseded)
- Closed with comment (if rejected)
- Labeled `disposition:defer` (if deferred)

---
```

## Active Dispositions (2024)

### Backlog Census (2026-05-01)

**Type**: Backlog Audit
**Scope**: Organization-wide
**Repositories Scanned**: 8 (forecast, xrtm.org, .github, train, eval, governance, xrtm, data)

**Results**:
- Open Pull Requests: 0
- Open Issues: 0
- Total Backlog Items: 0

**Evidence**:
- GitHub API search query: `org:xrtm-org is:open` (issues)
- GitHub API search query: `org:xrtm-org is:open` (pull requests)
- All repositories report `open_issues_count: 0` via GitHub API
- Scan timestamp: 2026-05-01 UTC

**Disposition**:
Clean backlog baseline established. No items requiring triage or disposition at this time.

**Next Steps**:
- Monitor for new PRs and issues
- Apply triage workflow when first contributions arrive
- Re-run census as part of periodic maintenance

---

### [forecast#123] Add parametric distribution support (2024-04-30)

**Disposition**: Accept with changes
**Scope**: Core Schema
**Priority**: High
**Risk**: High

**Rationale**:
Forecast Object v1.1 needs parametric distribution support for epistemic uncertainty modeling. The original PR had schema drift and lacked compatibility tests.

**Evidence**:
- Original PR tested against outdated schema version
- Missing backward compatibility shims for `confidence_interval`
- Validation gates required schema audit and compatibility layer

**Action Taken**:
- Accepted concept, superseded implementation with local changes
- Added compatibility tests between v1.0 and v1.1
- Merged as governance commit SHA a1b2c3d, forecast commit SHA e4f5g6h
- Updated `schemas/compatibility-policy.md` with migration notes

---

<!-- Add new entries above this line, newest first -->

## Archived Dispositions (Pre-2024)

_Historical decisions from before formalized triage process. Retained for reference._

---

## Usage Notes

### When to Log

Log every PR that is:
- Accepted (as-is or with changes)
- Superseded by local implementation
- Rejected or closed after review
- Deferred for future consideration

Do not log:
- Draft PRs that are abandoned by author without review request
- Duplicate PRs that are closed immediately without discussion
- Trivial typo fixes merged without debate

### Triage Workflow Integration

1. During triage, review open PRs against the [Triage Matrix](triage-matrix.md).
2. Apply [PR Acceptance Policy](pr-acceptance-policy.md) criteria.
3. Make disposition decision and record in this log with timestamp.
4. Update PR with comment explaining decision and next steps.
5. Apply appropriate disposition label: `disposition:accept`, `disposition:supersede`, `disposition:defer`, or `disposition:reject`.

### Periodic Cleanup

- **Monthly**: Review deferred items and re-evaluate priority.
- **Quarterly**: Archive old entries (older than 6 months) to prevent log bloat.
- **Annually**: Analyze patterns in rejections and defers to improve documentation or contribution guidelines.

### Log Maintenance

- Keep entries concise but complete.
- Link to PRs, commits, issues, and discussions rather than duplicating content.
- Use consistent terminology from governance glossary.
- Maintain reverse-chronological order (newest first) within each section.
