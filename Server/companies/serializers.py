from accounts.serializers import UserReturnStringSerializer
from companies.models import Companies, CompanyInviteList
from contacts.serializers import AddressSerializer, ContactSerializer
from general_ledger.serializers import GeneralLedgerNoCodeSerializer
from notes.serializers import CreateNoteSerializer, NotesNewlyCreatedSerializer
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


class CompanyNewlyCreatedSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of the Company model
    """

    business_address = AddressSerializer()
    mailing_address = AddressSerializer()
    contacts = ContactSerializer(many=True)
    gl_code = GeneralLedgerNoCodeSerializer()
    accounts_payable_gl = GeneralLedgerNoCodeSerializer()
    accounts_receivable_gl = GeneralLedgerNoCodeSerializer()
    allowed_admins = UserReturnStringSerializer(many=True)
    allowed_viewers = UserReturnStringSerializer(many=True)
    notes = NotesNewlyCreatedSerializer(many=True, read_only=True)

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
