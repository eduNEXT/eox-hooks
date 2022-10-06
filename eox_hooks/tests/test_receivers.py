"""This file contains all the test for the receivers.py file.

Classes:
    TestReceivers.
"""
import datetime

import attr
from django.conf import settings
from django.test import TestCase, override_settings
from mock import Mock, patch
from opaque_keys.edx.keys import CourseKey
from openedx_events.data import EventsMetadata
from openedx_events.learning.data import (
    CertificateData,
    CohortData,
    CourseData,
    CourseEnrollmentData,
    UserData,
    UserPersonalData,
)
from openedx_events.learning.signals import (
    CERTIFICATE_CHANGED,
    CERTIFICATE_CREATED,
    CERTIFICATE_REVOKED,
    COHORT_MEMBERSHIP_CHANGED,
    COURSE_ENROLLMENT_CHANGED,
    COURSE_ENROLLMENT_CREATED,
    COURSE_UNENROLLMENT_COMPLETED,
    SESSION_LOGIN_COMPLETED,
    STUDENT_REGISTRATION_COMPLETED,
)

from eox_hooks.receivers import hooks_handler


class TestReceivers(TestCase):
    """Receivers test class."""

    def setUp(self):
        """Set up class for Receivers testing."""
        self.sender = Mock()
        self.trigger_event = "sender.example"
        self.signal = Mock()

    @patch("eox_hooks.receivers._get_dispatch_uid")
    @patch("eox_hooks.receivers.action_handler")
    def test_trigger_response_action(self, action_handler, get_dispatch_uid):
        """
        Used to test that if USE_EOX_HOOKS is set to true then the handler triggers
        the execution of the action handlers.
        """
        get_dispatch_uid.return_value = ("eox-hooks:sender.example",)
        configuration = settings.EOX_HOOKS_DEFINITIONS.get(self.trigger_event)

        hooks_handler(self.sender, self.signal)

        action_handler.assert_called_once_with("sender.example", configuration, sender=self.sender)

    @patch("eox_hooks.receivers._get_dispatch_uid")
    @patch("eox_hooks.receivers.action_handler")
    def test_with_bad_uid(self, action_handler, get_dispatch_uid):
        """
        Used to test that if USE_EOX_HOOKS is set to true then the handler triggers
        the execution of the action handlers.
        """
        get_dispatch_uid.return_value = ("sender.example",)

        hooks_handler(self.sender, self.signal)

        action_handler.assert_not_called()

    @override_settings(USE_EOX_HOOKS=False)
    @patch("eox_hooks.receivers.action_handler")
    def test_not_trigger_response_action(self, action_handler):
        """
        Used to test that if USE_EOX_HOOKS is set to false then the handler won't trigger
        the execution of the action handlers.
        """
        hooks_handler(self.sender, self.signal)

        action_handler.assert_not_called()

    @override_settings(EOX_HOOKS_DEFINITIONS={})
    def test_without_hooks_configuration_defined(self):
        """
        Used to test what happends if the current tenant is using eox-hooks but there is not a
        configuration defined.

        This should result in the calling of a default action.
        """
        self.assertIsNone(hooks_handler(self.sender, self.signal))


@override_settings(USE_EOX_HOOKS=True)
class TestAuthEventsHandler(TestCase):
    """
    Tests for hooks_handler when receiving Open edX Events related to the auth process.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.user = UserData(
            pii=UserPersonalData(
                username="test",
                email="test@example.com",
                name="Test Example",
            ),
            id=39,
            is_active=True,
        )

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_register": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_registration(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        STUDENT_REGISTRATION_COMPLETED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.student.registration.completed.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        STUDENT_REGISTRATION_COMPLETED.connect(hooks_handler,
                                               dispatch_uid="eox-hooks:post_register")

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.user, action_handler.call_args.kwargs.get("user"))

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_session_login": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_login(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        SESSION_LOGIN_COMPLETED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.auth.session.login.completed.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        SESSION_LOGIN_COMPLETED.connect(hooks_handler, dispatch_uid="eox-hooks:post_session_login")

        SESSION_LOGIN_COMPLETED.send_event(
            user=self.user,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.user, action_handler.call_args.kwargs.get("user"))


class TestEnrollmentEventsHandler(TestCase):
    """
    Tests for hooks_handler when receiving Open edX Events related to the enrollment process.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.enrollment = CourseEnrollmentData(
            user=UserData(
                pii=UserPersonalData(
                    username="test",
                    email="test@example.com",
                    name="Test Example",
                ),
                id=39,
                is_active=True,
            ),
            course=CourseData(
                course_key=CourseKey.from_string("course-v1:edX+DemoX+Demo_Course"),
                display_name="Demonstration Course",
            ),
            mode="audit",
            is_active=True,
            creation_date=datetime.datetime.now(),
        )

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_enrollment": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_enrollment(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        COURSE_ENROLLMENT_CREATED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.course.enrollment.created.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        COURSE_ENROLLMENT_CREATED.connect(hooks_handler, dispatch_uid="eox-hooks:post_enrollment")

        COURSE_ENROLLMENT_CREATED.send_event(
            enrollment=self.enrollment,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.enrollment, action_handler.call_args.kwargs.get("enrollment"))

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_enrollment_change": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_enroll_change(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        COURSE_ENROLLMENT_CHANGED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.course.enrollment.changed.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        COURSE_ENROLLMENT_CHANGED.connect(hooks_handler,
                                          dispatch_uid="eox-hooks:post_enrollment_change")

        COURSE_ENROLLMENT_CHANGED.send_event(
            enrollment=self.enrollment,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.enrollment, action_handler.call_args.kwargs.get("enrollment"))

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_unenrollment": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_unenrollment(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        COURSE_UNENROLLMENT_COMPLETED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.course.unenrollment.completed.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        COURSE_UNENROLLMENT_COMPLETED.connect(hooks_handler,
                                              dispatch_uid="eox-hooks:post_unenrollment")

        COURSE_UNENROLLMENT_COMPLETED.send_event(
            enrollment=self.enrollment,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.enrollment, action_handler.call_args.kwargs.get("enrollment"))


class TestCertificateEventsHandler(TestCase):
    """
    Tests for hooks_handler when receiving Open edX Events related to the certification process.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.certificate = CertificateData(
            user=UserData(
                pii=UserPersonalData(
                    username="test",
                    email="test@example.com",
                    name="Test Example",
                ),
                id=39,
                is_active=True,
            ),
            course=CourseData(
                course_key=CourseKey.from_string("course-v1:edX+DemoX+Demo_Course"),
                display_name="Demonstration Course",
            ),
            mode="audit",
            current_status="notpassing",
            grade=100,
            download_url="https://downdloadurl.com",
            name="Certs",
        )

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_certificate_creation": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_cert_creation(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        CERTIFICATE_CREATED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.certificate.created.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        CERTIFICATE_CREATED.connect(hooks_handler,
                                    dispatch_uid="eox-hooks:post_certificate_creation")

        CERTIFICATE_CREATED.send_event(
            certificate=self.certificate,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.certificate, action_handler.call_args.kwargs.get("certificate"))

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_certificate_change": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_cert_change(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        CERTIFICATE_CHANGED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.certificate.changed.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        CERTIFICATE_CHANGED.connect(hooks_handler, dispatch_uid="eox-hooks:post_certificate_change")

        CERTIFICATE_CHANGED.send_event(
            certificate=self.certificate,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.certificate, action_handler.call_args.kwargs.get("certificate"))

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_certificate_revoke": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_cert_revoked(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        CERTIFICATE_REVOKED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.certificate.revoked.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        CERTIFICATE_REVOKED.connect(hooks_handler, dispatch_uid="eox-hooks:post_certificate_revoke")

        CERTIFICATE_REVOKED.send_event(
            certificate=self.certificate,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.certificate, action_handler.call_args.kwargs.get("certificate"))


class TestCohortEventsHandler(TestCase):
    """
    Tests for hooks_handler when receiving Open edX Events related to the cohort process.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.cohort = CohortData(
            user=UserData(
                pii=UserPersonalData(
                    username="test",
                    email="test@example.com",
                    name="Test Example",
                ),
                id=39,
                is_active=True,
            ),
            course=CourseData(
                course_key=CourseKey.from_string("course-v1:edX+DemoX+Demo_Course"),
                display_name="Demonstration Course",
            ),
            name="Uchiha",
        )

    @override_settings(EOX_HOOKS_DEFINITIONS={"post_cohort_change": {}})
    @patch("eox_hooks.receivers.action_handler")
    def test_receiver_called_after_cert_change(self, action_handler):
        """
        Test that hooks_handler is called the correct information after sending
        COHORT_MEMBERSHIP_CHANGED event.
        """
        metadata = EventsMetadata(
            event_type="org.openedx.learning.cohort_membership.changed.v1",
            minorversion=0,
        )
        expected_metadata_subset = {
            "event_type": metadata.event_type,
            "minorversion": metadata.minorversion,
            "source": metadata.source,
            "sourcehost": metadata.sourcehost,
            "sourcelib": list(metadata.sourcelib),
        }
        action_handler.return_value.__name__ = "receiver"
        action_handler.return_value.__module__ = "receiver_module"
        COHORT_MEMBERSHIP_CHANGED.connect(hooks_handler,
                                          dispatch_uid="eox-hooks:post_cohort_change")

        COHORT_MEMBERSHIP_CHANGED.send_event(
            cohort=self.cohort,
        )

        self.assertDictContainsSubset(
            expected_metadata_subset, attr.asdict(action_handler.call_args.kwargs.get("metadata")),
        )
        self.assertEqual(self.cohort, action_handler.call_args.kwargs.get("cohort"))
