# CHANGELOG

<!-- version list -->

## v1.1.3 (2026-10-06)

### Bug Fixes

- Persist control endpoint in a typed recovery journal
  ([#10](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/10),
  [`808b4c1`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/808b4c1a3274b114ce0bb28aa990051f27980542))

### Chores

- Add flake8 linting
  ([`d09c44f`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/d09c44f6810c453eb99d8a75fd9f2e58813765e9))

- Remove bump_readme_pin script and update AGENTS instructions
  ([#8](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/8),
  [`400d647`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/400d6471f131e29b4d33d20923317f53648eda6c))

- Remove test for bump_readme_pin script
  ([#8](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/8),
  [`400d647`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/400d6471f131e29b4d33d20923317f53648eda6c))

### Continuous Integration

- Add coverage and README badges
  ([`16b82b8`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/16b82b8329e0ee5e1c4c0459e6b2e09383e975e5))

### Documentation

- Fix coverage badge
  ([`9a81723`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/9a81723ee726337e8de37ba7f8cbb594fa67d9e5))

### Refactoring

- Separate module concerns and simplify deployment code
  ([#7](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/7),
  [`e9b847b`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/e9b847bb200f0d46b7d65b85bee93270ba92ea45))

### Testing

- Split tests per module and tighten names and assertions
  ([#9](https://github.com/alvarog2491/agentcore-ab-release-gate/pull/9),
  [`332c018`](https://github.com/alvarog2491/agentcore-ab-release-gate/commit/332c0189997aee2eb7cb75b85ff6973004234bba))


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
