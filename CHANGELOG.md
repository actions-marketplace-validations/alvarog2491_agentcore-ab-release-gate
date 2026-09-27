# CHANGELOG

<!-- version list -->

## v1.1.2 (2026-09-27)

### Bug Fixes

- Raise named exceptions with clear messages
  ([#6](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/6),
  [`180d61f`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/180d61f96ab702927aa12fe53dd9fc9407f5038c))

### Chores

- Add CODEOWNERS file to define repository ownership
  ([#5](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/5),
  [`0738ae4`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/0738ae4c56f243906ac434233a77266f130c49ba))

### Continuous Integration

- Keep uv.lock in sync with the released project version
  ([#4](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/4),
  [`2e630e9`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/2e630e9e2085809dc4dcec077f105fd20368d8f4))

- Update uv version to 0.12.19 and adjust action configuration
  ([#4](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/4),
  [`2e630e9`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/2e630e9e2085809dc4dcec077f105fd20368d8f4))


## v1.1.1 (2026-09-25)

### Bug Fixes

- Report respects require-significance when rendering gate results
  ([#3](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/3),
  [`af41761`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/af41761a647571e75f2a0299017e19d3ede26d2c))

- Streamline report rendering by consolidating string formatting
  ([#3](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/3),
  [`af41761`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/af41761a647571e75f2a0299017e19d3ede26d2c))


## v1.1.0 (2026-09-25)

### Continuous Integration

- Push releases with a token that can bypass the main ruleset
  ([#2](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/2),
  [`ef37fe9`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/ef37fe94162d15f3cfbe0b22bb95fb5ee7c0d8d6))

### Documentation

- Add CLAUDE.md for project guidance and command instructions
  ([`6cc1557`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/6cc15574ab20925370a1bbe5256b177074c329a7))

- Replace CLAUDE.md for AGENTS.md (claude version 2.1.278)
  ([`571d256`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/571d2565e75e97fc53ae71a2078e503ae5da4523))

### Features

- Validate inputs with Pydantic, install via uv, and automate releases
  ([#1](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/1),
  [`5290ed3`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/5290ed3efa4827c9fcb6e40e68e915767fe4f7b8))

### Refactoring

- Remove duplicated logic in deployment and evaluation
  ([#1](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/1),
  [`5290ed3`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/5290ed3efa4827c9fcb6e40e68e915767fe4f7b8))

### Testing

- Close coverage gaps in polling, reporting, and CLI wiring
  ([#1](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/1),
  [`5290ed3`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/5290ed3efa4827c9fcb6e40e68e915767fe4f7b8))


## v1.0.0 (2026-09-21)

- Initial Release
