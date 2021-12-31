from companies.models import Companies
from companies.serializers import (
    CompanyCreationSerializer,
    CompanyNewlyCreatedSerializer,
    CompanyInviteList,
)
from contacts.functions import populate_address_dict
from contacts.models import Addresses, Contacts
from django.db import transaction
from general_ledger.models import GeneralLedgerCodes
from notes.models import Notes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class CompanyCreationViewSet(generics.CreateAPIView):
    """
    Viewset responsible for the creation of a company.

    New companies automatically get 3 general ledgers associated with them. Accounts receivable, accounts payable, and company specific general ledger account.
    """

    queryset = Companies.objects.all()
    serializer_class = CompanyCreationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        # Serialize the data
        serializer = self.get_serializer(data=request.data)

        # Creates a valid address dictionary to be validated against.
        # Accounts for None or missing values
        serializer.initial_data["business_address"] = populate_address_dict(
            None
            if ("business_address" not in serializer.initial_data)
            or (serializer.initial_data["business_address"] is None)
            else serializer.initial_data["business_address"]
        )

        # Creates a valid address dictionary to be validated against.
        # Accounts for None or missing values
        serializer.initial_data["mailing_address"] = populate_address_dict(
            None
            if ("mailing_address" not in serializer.initial_data)
            or (serializer.initial_data["mailing_address"] is None)
            else serializer.initial_data["mailing_address"]
        )

        # Fail-safe to make sure a contacts array is included
        if "contacts" not in serializer.initial_data:
            serializer.initial_data["contacts"] = []

        # Fail-safe to make sure a notes array is included
        if "notes" not in serializer.initial_data:
            serializer.initial_data["notes"] = []

        # Validates all fields. Return the errors if any are found.
        if not serializer.is_valid():
            return Response(
                {"company-errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Pop out the business address information
        business_address = serializer.validated_data.pop("business_address")

        # Pop out the mailing address information
        mailing_address = serializer.validated_data.pop("mailing_address")

        # Pop out the contact list if provided
        if "contacts" in serializer.validated_data:
            contact_list = serializer.validated_data.pop("contacts")
        # Otherwise, set a blank contacts array in the serializer
        # and a blank contact_list array for later processing
        else:
            serializer.validated_data["contacts"] = []
            contact_list = []

        # Pop out company notes if provided
        company_notes = serializer.validated_data.pop("notes")

        # Make all the posts behind an atomic transaction to make sure
        # all entries are successfully made
        with transaction.atomic():

            # Check if any business address values are present
            if any(business_address.values()):
                # Save the business address
                business_address_obj = Addresses.objects.create(**business_address)
            # If all values are blank, save a None value
            else:
                business_address_obj = None

            # Check if any mailing address values are present
            if any(mailing_address.values()):
                # Save the mailing address
                mailing_address_obj = Addresses.objects.create(**mailing_address)
            # If all values are blank, save a None value
            else:
                mailing_address_obj = None

            # Create the encompassing accounts receivable general ledger
            accounts_receivable_gl = GeneralLedgerCodes.objects.create(
                name="Accounts Receivable",
                description=f"Accounts Receivable ledger for {serializer.validated_data['business_name']}",
            )

            # Create the encompassing accounts payable general ledger
            accounts_payable_gl = GeneralLedgerCodes.objects.create(
                name="Accounts Payable",
                description=f"Accounts Payable ledger for {serializer.validated_data['business_name']}",
            )

            # Create the general ledger account for company expenses
            gl_code = GeneralLedgerCodes.objects.create(
                name=f"{serializer.validated_data['business_name']}",
                description=f"{serializer.validated_data['business_name']} general ledger",
            )

            # Save the company with all the newly created address and gl_code objects
            company_obj = serializer.save(
                business_address=business_address_obj,
                mailing_address=mailing_address_obj,
                accounts_payable_gl=accounts_payable_gl,
                accounts_receivable_gl=accounts_receivable_gl,
                gl_code=gl_code,
            )

            # If contacts are present, loop through each contact
            for contact in contact_list:
                # Create the contact
                contact_obj = Contacts.objects.create(**contact)
                # Add that contact object to the ManyToMany contacts field
                company_obj.contacts.add(contact_obj)

            # If notes are present, loop through each note
            for company_note in company_notes:
                # Assign the user to the note
                company_note["user"] = request.user
                # Create the note with associated user
                company_note_obj = Notes.objects.create(**company_note)
                # Add that note object to the ManyToMany notes field
                company_obj.notes.add(company_note_obj)

            # Add the current user as an allowed admin
            company_obj.allowed_admins.add(request.user)

        # Set the response headers
        headers = self.get_success_headers(company_obj)

        return Response(
            data=CompanyNewlyCreatedSerializer(company_obj).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


##############################################
#      Invite User To Company Viewset        #
##############################################


class CompanyInviteUserViewSet(generics.CreateAPIView):
    """
    Save a user email to the table and which company they are invited to with a role of either admin or viewer
    """

    queryset = CompanyInviteList.objects.all()
    serializer_class = CompanyInviteList
    permission_classes = (IsAuthenticated,)

    def send_bad_invite_response(self, company_id=None):
        """
        Generic error response for invalid invite request.

        Used for invalid companies or users sending invites to companies they do not have admin_in status in
        """
        return {
            "invite-error": "can not send invite to requested company",
            "detail": f"Can not invite user to company with ID {company_id}",
        }

    def create(self, request, **kwargs):
        # Check that the company exist
        try:
            company_obj = Companies.objects.get(pk=kwargs["pk"])
        except Companies.DoesNotExist:
            # If the company does not exist, return generic response
            return Response(
                data=self.send_bad_invite_response(kwargs["pk"]),
                status=status.HTTP_400_BAD_REQUEST,
            )

        print(
            company_obj.allowed_admins.filter(pk=request.user.pk).exists(),
            ">>>>>>>>>>>>>>>>>>>>>>>",
        )

        return Response({})
