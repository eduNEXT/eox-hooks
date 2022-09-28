"""
Serializers for actions.
"""
import json

from django.contrib.auth import get_user_model
from rest_framework import serializers

from eox_hooks.edxapp_wrapper.models import get_certificate_model, get_user_profile_model

GeneratedCertificate = get_certificate_model()
UserProfile = get_user_profile_model()


class CertificateSerializer(serializers.ModelSerializer):
    """
    Serializes GeneratedCertificate models
    """
    created_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:  # pylint: disable=R0903
        """Meta class."""
        model = GeneratedCertificate
        fields = '__all__'


class RetirementUserProfileSerializer(serializers.ModelSerializer):
    """
    Serialize a small subset of UserProfile data.
    """
    country = serializers.CharField(read_only=True)
    meta = serializers.SerializerMethodField(read_only=True)

    class Meta:  # pylint: disable=R0903
        """Meta class."""
        model = UserProfile
        fields = '__all__'

    def get_meta(self, obj):
        """Return meta field as dict."""
        try:
            meta = json.loads(obj.meta)
        except ValueError:
            meta = {}
        return meta


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User models
    """
    profile = RetirementUserProfileSerializer(read_only=True)

    class Meta:  # pylint: disable=R0903
        """Meta class."""
        model = get_user_model()
        exclude = ['password']


class CourseSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Course objects providing minimal data about the course.
    """

    id = serializers.CharField()
    name = serializers.CharField(source='display_name_with_default_escaped')
    number = serializers.CharField(source='display_number_with_default')
    org = serializers.CharField(source='display_org_with_default')
    other_course_settings = serializers.SerializerMethodField(read_only=True)
    cert_html_view_overrides = serializers.DictField()

    def get_other_course_settings(self, obj):
        """Return other course settings"""
        return getattr(obj, 'other_course_settings', {})
