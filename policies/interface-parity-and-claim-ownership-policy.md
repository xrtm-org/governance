# Interface Parity and Claim Ownership Policy

This policy defines how XRTM treats CLI, WebUI, TUI, and API surfaces when a
capability is presented as part of the product. Use it with the release
readiness, feature graduation, cross-repo compatibility, and stack versioning
policies.

## Product rule

Released product tasks should not require users to discover that one interface
is the "real" product and another is only a partial demo.

For every released product capability, the owning repo must record one explicit
interface status:

| Status | Meaning | Allowed claims |
| --- | --- | --- |
| `parity-ready` | CLI and WebUI expose the same released capability with interface-appropriate controls and shared service semantics. | Release-pinned docs may say users can choose either CLI or WebUI for that task. |
| `cli-only-accepted` | The capability is intentionally terminal-only for now, with a documented reason and graduation condition. | Release-pinned docs may describe the CLI path, but must not imply WebUI parity. |
| `webui-only-accepted` | The capability is intentionally browser-only for now, with a documented reason and graduation condition. | Release-pinned docs may describe the WebUI path, but must not imply CLI parity. |
| `interface-entrypoint` | The command or route launches, inspects, or switches interfaces rather than representing a product capability itself. | Docs may explain the entrypoint without requiring a mirror entrypoint in another interface. |
| `advanced/experimental` | The capability exists but is not part of the default released product path. | Advanced docs only, with explicit labeling and no default-path parity claim. |
| `redesign-required` | The current behavior works technically but should not become the public contract. | Keep out of release-pinned docs and parity claims until the contract is redesigned. |

## Source-of-truth records

1. `governance` owns this policy and the shared vocabulary.
2. `xrtm` owns the implementation-level parity matrix for product-shell
   commands, WebUI routes, product services, and release gates.
3. `xrtm.org` mirrors released truth after `xrtm` has implementation evidence
   and an updated release contract.
4. Support packages own their package APIs and metadata. They do not need WebUI
   parity records unless `xrtm` exposes their behavior as a top-level product
   task.

The implementation-level matrix must identify:

1. the CLI command or command family
2. the WebUI route, API route, or module that exposes the same capability
3. the current interface status
4. the persona or user job served
5. the shared product service that owns behavior
6. the docs owner and release-pinned claim owner
7. the required Gate 1, Gate 2, or Gate 3 evidence

## Shared service rule

Parity is not satisfied by copying CLI behavior into a separate WebUI code path.
Mutating or release-critical WebUI actions must call the same product service
semantics used by CLI commands, or a documented shared adapter that has parity
tests against the CLI behavior.

Examples of release-critical actions include:

1. starting a first-success run
2. running or validating a workflow
3. generating reports
4. exporting run evidence
5. creating or running profiles
6. starting or changing monitor state
7. cleaning artifacts

## Claim rules

1. Release-pinned docs may claim CLI/WebUI choice only for `parity-ready`
   capabilities.
2. If a capability is CLI-only, WebUI-only, advanced, or redesign-required, the
   page must say so or keep it out of the default released path.
3. Public site pages must not introduce parity claims before the product repo
   has the matrix update, implementation, contract update where needed, and
   release evidence.
4. A parity claim is a stable product-surface claim. If it changes user-visible
   behavior, apply the cross-repo compatibility policy and coordinate docs,
   contracts, and site updates.

## Gate requirements

Gate 1 for every parity PR must include the repo-local checks plus any changed
service-level parity tests. For `xrtm`, this means the normal lint, type, test,
WebUI build, package, installed-wheel, and command-claim checks appropriate to
the touched surface.

Gate 2 is required before releasing a user-facing parity expansion in `xrtm`.
It must validate the WebUI-only path from a fresh install for the released task,
not just prove the CLI command still works. If the released claim depends on a
real OpenAI-compatible endpoint or coding-agent CLI contract, Gate 2 must include
the corresponding supported runtime profile under the release-readiness policy.

Gate 3 is for broad provider, corpus, scale, benchmark, stress, and competition
coverage. Do not make Gate 3 the default PR merge blocker unless the release
promise depends on that advanced path.

## Graduation process

1. Add or update the implementation-level parity matrix before broadening public
   claims.
2. Implement missing service/API/frontend behavior behind shared product
   services.
3. Add service-level parity tests and WebUI route/API smoke for the changed
   capability.
4. Promote docs and release-command contracts only with release evidence.
5. Mirror the released claim on `xrtm.org` last.

If any evidence fails or the behavior is semantically unclear, keep the item
`cli-only-accepted`, `advanced/experimental`, or `redesign-required` rather than
presenting partial parity as complete.
