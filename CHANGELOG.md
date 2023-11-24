# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v5.1.0 - 2023-11-24

### [5.1.0](https://github.com/eduNEXT/eox-hooks/compare/v5.0.0...v5.1.0) (2023-11-24)

#### Features

- add Lilac backend ([#46](https://github.com/eduNEXT/eox-hooks/issues/46)) ([c196b2d](https://github.com/eduNEXT/eox-hooks/commit/c196b2df99f43eff0df1bdc2a752e81d45dcb8e0))

## v5.0.0 - 2023-11-20

### [5.0.0](https://github.com/eduNEXT/eox-hooks/compare/v4.1.1...v5.0.0) (2023-11-20)

#### ⚠ BREAKING CHANGES

- add palm support

#### Performance Improvements

- palm release support ([#45](https://github.com/eduNEXT/eox-hooks/issues/45)) ([08c4cc0](https://github.com/eduNEXT/eox-hooks/commit/08c4cc093874c0e72beb996348a7faeeaaf707e5))

## v4.1.1 - 2023-06-21

### [4.1.1](https://github.com/eduNEXT/eox-hooks/compare/v4.1.0...v4.1.1) (2023-06-21)

### Bug Fixes

- valitade enrollment for programs ([#42](https://github.com/eduNEXT/eox-hooks/issues/42)) ([c4711a9](https://github.com/eduNEXT/eox-hooks/commit/c4711a909cc35a83cfede41c4dd466b9eb2c9dd9))

## v4.1.0 - 2023-05-10

### [4.1.0](https://github.com/eduNEXT/eox-hooks/compare/v4.0.0...v4.1.0) (2023-05-10)

#### Features

- allow a child course to belong to multiples parents ([#41](https://github.com/eduNEXT/eox-hooks/issues/41)) ([1bb9700](https://github.com/eduNEXT/eox-hooks/commit/1bb9700cf4bd19e59b2ae0714f567855bfacddad))

#### Continuous Integration

- Update issue templates ([6293c3c](https://github.com/eduNEXT/eox-hooks/commit/6293c3cd03fc79fbeadcc6eaf2d9b05c99cd1931))

## v4.0.0 - 2023-01-30

### [4.0.0](https://github.com/eduNEXT/eox-hooks/compare/v3.0.1...v4.0.0) (2023-01-30)

#### ⚠ BREAKING CHANGES

- **DS-367:** add compatibility with olive

#### Features

- **DS-367:** add compatibility with Open edX olive release ([#39](https://github.com/eduNEXT/eox-hooks/issues/39)) ([887bf2c](https://github.com/eduNEXT/eox-hooks/commit/887bf2c20dc66680f200cf1d385e2473240bd954))

## v3.0.1 - 2023-01-10

### [3.0.1](https://github.com/eduNEXT/eox-hooks/compare/v3.0.0...v3.0.1) (2023-01-10)

### Bug Fixes

- adding a fake request to execute in async servers ([#35](https://github.com/eduNEXT/eox-hooks/issues/35)) ([0fbf12e](https://github.com/eduNEXT/eox-hooks/commit/0fbf12e6ee331eef764e3b802db38cd5c786380a))

### Continuous Integration

- adds mantainer group ([#37](https://github.com/eduNEXT/eox-hooks/issues/37)) ([b8c8596](https://github.com/eduNEXT/eox-hooks/commit/b8c859638ea2cb68803f2a7a715811a0abb7e40a))
- update the changelog updater step in bumpversion ([#36](https://github.com/eduNEXT/eox-hooks/issues/36)) ([563dd82](https://github.com/eduNEXT/eox-hooks/commit/563dd825228495170ebdd90b0ce0f752bc1f2291))

## v3.0.0 - 2022-10-06

### [3.0.0](https://github.com/eduNEXT/eox-hooks/compare/v2.0.1...v3.0.0) (2022-10-06)

#### ⚠ BREAKING CHANGES

- Drop python 3.5 support in favor of python 3.8.

#### Features

- add support to nutmeg ([385e8c2](https://github.com/eduNEXT/eox-hooks/commit/385e8c2ca987185d42f4a079be7e043e4fdb238b))

## [2.0.1] - 2022-06-28

### Added

- Add more descriptive message when action fails.

## [2.0.0] - 2021-11-17

### Added

- **BREAKING CHANGE**: add support for lilac and therefore changed backends defaults.
- **BREAKING CHANGE**: add support for openedx-events. Only works for Lilac with PRs backport 28266 and 18640
- and >= Maple.

## [1.0.0] - 2021-08-17

### Added

- Drop support for python 2.7.
- Add backends for course, enrollment and course modes.
- Add custom action and task used to enroll users into program courses.
- Add action that propagates grade to course programs

## [0.5.0] - 2021-04-13

### Added

- Added post_register signal configuration.

## [0.4.0] - 2021-02-18

### Added

- Added post_to_webhook_url action.

## [0.3.0] - 2020-11-11

### Added

- First release on PyPI.

## [0.2.1] - 2020-10-29

### Added

- Allow install plugin without existent signal_paths.

## [0.2.0] - 2020-08-04

### Added

- Added trigger/action handlers for defined hooks.

## [0.1.0] - 2020-07-08
