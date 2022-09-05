# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2022-06-28

### Added

- Add more descriptive message when action fails.

## [2.0.0] - 2021-11-17

### Added

- **BREAKING CHANGE**: add support for lilac and therefore changed backends defaults.
- **BREAKING CHANGE**: add support for openedx-events. Only works for Lilac with PRs backport 28266 and 18640
  and >= Maple.

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

