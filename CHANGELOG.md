# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v8.1.0](https://github.com/eduNEXT/eox-hooks/compare/v8.0.0...v8.1.0) - (2025-06-09)

### Changed

- **Teak Support**: Upgrade requirements base on edx-platform Teak

## [v8.0.0](https://github.com/eduNEXT/eox-hooks/compare/v7.0.0...v8.0.0) - (2024-12-13)

### Changed

- **Sumac Support**: Removed support for Python 3.8. Upgrade requirements base on edx-platform Sumac
  release update GitHub workflows and actions version, and update integration test to use new Sumac release with Tutor.

## [v7.0.0](https://github.com/eduNEXT/eox-hooks/compare/v6.3.0...v7.0.0) - (2024-11-20)

#### ⚠ BREAKING CHANGES

- **Dropped Support for Django 3.2**: Removed support for Django 3.2 in this plugin. As a result, we have also dropped support for Open edX releases from Maple up to and including Palm, which rely on Django 3.2. Future versions of this plugin may not be compatible with these Open edX releases.

## [v6.3.0](https://github.com/eduNEXT/eox-hooks/compare/v6.2.0...v6.3.0) - (2024-07-24)

### Added

- **Integration Tests**: A new GitHub workflow has been added to run
  integration tests. These tests validate backend imports and ensure the
  `/eox-info` endpoint functions correctly.

### Changed

- **Redwood Support**: Upgrade requirements base on edx-platform redwood
  release update GitHub workflows with new Python (3.10 and 3.11) and actions
  version, and update integration test to use new redwood release with Tutor.

## v6.2.0 - 2024-05-24

### [6.2.0](https://github.com/eduNEXT/eox-hooks/compare/v6.1.0...v6.2.0) (2024-05-24)

#### Features

* add test integration ([#50](https://github.com/eduNEXT/eox-hooks/issues/50)) ([bfad685](https://github.com/eduNEXT/eox-hooks/commit/bfad685339eb4e5214596ffe57d9ef3c827c80d5))

## v6.1.0 - 2024-03-19

### [6.1.0](https://github.com/eduNEXT/eox-hooks/compare/v6.0.0...v6.1.0) (2024-03-19)

#### Features

* add workflow to add items to the Dedalo project DS-831 ([#49](https://github.com/eduNEXT/eox-hooks/issues/49)) ([54c66db](https://github.com/eduNEXT/eox-hooks/commit/54c66db9b474df85187eb01bace630b376eb95a4))

## v6.0.0 - 2024-02-09

### [6.0.0](https://github.com/eduNEXT/eox-hooks/compare/v5.1.0...v6.0.0) (2024-02-09)

#### ⚠ BREAKING CHANGES

* Quince release support
  
* fix(import): update URLs in favor of re_path for deprecation
  
* perf: update requirements
  
* fix: remove 3.10 version test
  
* perf: update workflows and readme
  
* fix: fix AttributeError to non-string uid
  
* perf: update tests
  
* perf:  update codelytv/pr-size-labeler
  
* perf: add django32, django42 file requirements
  
* perf: update Django version constrain
  
* fix: update python test version
  
* perf: update readme and constraints
  
* perf: update constraints
  
* perf: update requirements
  
* perf: update tox
  
* fix: update actions/setup-python version
  
* perf: quince release support (#48) ([3a330d7](https://github.com/eduNEXT/eox-hooks/commit/3a330d70cb21fabe3381e3cc2aeb120b7a93955e)), closes [#48](https://github.com/eduNEXT/eox-hooks/issues/48)
  

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
