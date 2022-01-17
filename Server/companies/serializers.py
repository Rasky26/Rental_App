from accounts.serializers import UserReturnStringSerializer, UsernameSerializer
from companies.models import Companies, CompanyInviteList
from contacts.serializers import AddressSerializer, ContactSerializer
from datetime import datetime, timedelta
from documents.models import Documents
from documents.serializers import (
    DocumentCreationSerializer,
    DocumentSerializer,
    ImageSerializer,
)
from general_ledger.serializers import GeneralLedgerNoCodeSerializer
from notes.serializers import CreateNoteSerializer, NotesSerializer
from rest_framework import serializers


class CompanyCreationSerializer(serializers.ModelSerializer):
    """
    Serializes the Company model for creation.
    """

    business_address = AddressSerializer()
    mailing_address = AddressSerializer()
    contacts = ContactSerializer(many=True)
    notes = CreateNoteSerializer(many=True)

    class Meta:
        model = Companies
        fields = (
            "business_name",
            "legal_name",
            "business_address",
            "mailing_address",
            "contacts",
            "notes",
        )


class CompanyFullAdminSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of the Company model.

    Should be used with allowed_admins users due to comprehensive nature.
    """

    business_address = AddressSerializer()
    mailing_address = AddressSerializer()
    contacts = ContactSerializer(many=True)
    gl_code = GeneralLedgerNoCodeSerializer()
    accounts_payable_gl = GeneralLedgerNoCodeSerializer()
    accounts_receivable_gl = GeneralLedgerNoCodeSerializer()
    allowed_admins = UsernameSerializer(many=True)
    allowed_viewers = UsernameSerializer(many=True)
    documents = DocumentSerializer(many=True)
    images = ImageSerializer(many=True)
    notes = NotesSerializer(many=True, read_only=True)

    class Meta:
        model = Companies
        fields = (
            "id",
            "business_name",
            "legal_name",
            "business_address",
            "mailing_address",
            "contacts",
            "gl_code",
            "accounts_payable_gl",
            "accounts_receivable_gl",
            "allowed_admins",
            "allowed_viewers",
            "documents",
            "images",
            "notes",
            "accounts_payable_extension",
            "accounts_receivable_extension",
            "maintenance_extension",
        )


##############################################
#     Invite User To Company Serializer      #
##############################################


class CompanyInviteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInviteList
        fields = (
            "email",
            "admin_in",
            "viewer_in",
        )


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ("company_name",)


class CompanyInviteListActiveSerializer(serializers.ModelSerializer):
    admin_in = CompanyNameSerializer(many=False, read_only=True)
    viewer_in = CompanyNameSerializer(many=False, read_only=True)
    valid_until = serializers.SerializerMethodField(method_name="get_valid_until")

    class Meta:
        model = CompanyInviteList
        fields = (
            "email",
            "admin_in",
            "viewer_in",
            "valid_until",
        )

    def get_valid_until(self, obj):
        return (obj.updated_at + timedelta(days=7)).strftime(
            "%b. %d, %Y - %I:%M %p UTC"
        )


##############################################
#   Upload Document To Company Serializer    #
##############################################


class CompanyUploadDocumentsSerializer(serializers.ModelSerializer):
    """
    Serializes documents to be attached to a specific company
    """

    # notes = CreateNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Documents
        fields = (
            "name",
            "document",
            # "uploaded_by",
            # "notes",
        )
