Change Log
==========

..
   All enhancements and patches to eox_hooks will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).
   
   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.
Unreleased
----------

[2.0.0] - 2021-11-17
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **BREAKING CHANGE**: add support for lilac and therefore changed backends defaults.
* **BREAKING CHANGE**: add support for openedx-events. Only works for Lilac with PRs backport 28266 and 18640
  and >= Maple.

[1.0.0] - 2021-08-17
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Drop support for python 2.7.
* Add backends for course, enrollment and course modes.
* Add custom action and task used to enroll users into program courses.
* Add action that propagates grade to course programs

[0.5.0] - 2021-04-13
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added post_register signal configuration.

[0.4.0] - 2021-02-18
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added post_to_webhook_url action.

[0.3.0] - 2020-11-11
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* First release on PyPI.


[0.2.1] - 2020-10-29
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Allow install plugin without existent signal_paths.

[0.2.0] - 2020-08-04
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added trigger/action handlers for defined hooks.

[0.1.0] - 2020-07-08
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

