# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
