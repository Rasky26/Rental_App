from accounts.models import User
from companies.models import Companies, CompanyInviteList
from companies.serializers import (
    CompanyFullAdminSerializer,
    CompanyCreationSerializer,
    CompanyInviteListActiveSerializer,
    CompanyInviteListSerializer,
    CompanyUploadDocumentsSerializer,
)
from contacts.functions import populate_address_dict, populate_contact_dict
from contacts.models import Addresses, Contacts
from django.db import transaction
from django.db.models import Q
from general_ledger.models import GeneralLedgerCodes
from notes.models import Notes
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.


def send_invalid_permission_response(requested_level=None, level_id=None):
    """
    Generic error response for invalid permission levels.

    Used for invalid companies or users sending invites to companies they do not have admin_in status in
    """
    return {
        "invite-error": f"invalid invite permissions for requested {requested_level}",
        "detail": f"Can not invite user to company with ID {level_id}",
    }


class CompanyCreationViewSet(generics.CreateAPIView):
    """
    Viewset responsible for the creation of a company.

    New companies automatically get 3 general ledgers associated with them. Accounts receivable, accounts payable, and company specific general ledger account.
    """

    queryset = Companies.objects.all()
    serializer_class = CompanyCreationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):

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
                # Clean-up the contact information
                contact = populate_contact_dict(contact)
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
            data=CompanyFullAdminSerializer(company_obj).data,
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
    serializer_class = CompanyInviteListSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, **kwargs):
        """
        Manages the company invite request methods. Cleans the database of expired invites, then does the following:

        1.) Ensure the company exists
        2.) Verify the request user has 'allowed_admins' privilege in company
        3.) Check that the request is for EITHER admin_in OR viewer_in, not BOTH
        4.) If the requested email has an associated User model object, check if that object exists in the company permissions
            4.1) If user is admin in company and admin role requested, do not send invite
            4.2) If user is viewer in company and admin role requested, send invite
            4.3) If user is admin in company and viewer role requested, do not send invite - (handle via company role manager)
            4.4) If user is viewer in company and viewer role requested, do not send invite
        <If not step 4>
        5.) Inspect invites for existing records
            5.1) If email does not have current admin or viewer invites and an admin is requested, send invite
            5.2) If email has an admin invite and a viewer role requested, do not send invite
                5.3) Inform request.user of the current active invite
        """

        # Clean the invite database of timed-out invites
        # Get a list of all the expired invites
        expired_invite_ids = [obj.id for obj in self.queryset.all() if obj.timeout]
        # Delete those rows
        self.queryset.filter(id__in=expired_invite_ids).delete()

        # Check that the company exist
        try:
            company_obj = Companies.objects.get(pk=kwargs["pk"])

        # If the company does not exist, return generic response

        except Companies.DoesNotExist:
            return Response(
                data=send_invalid_permission_response(
                    requested_level="company", level_id=kwargs["pk"]
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check that the requesting user is set as an admin for the indicated company
        if not company_obj.allowed_admins.filter(pk=request.user.pk).exists():
            return Response(
                data=send_invalid_permission_response(
                    requested_level="company", level_id=kwargs["pk"]
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verify there is one False and one True item in the request.data.
        # Sort the information for easier comparison
        if sorted([request.data["admin_in"], request.data["viewer_in"]]) != [
            False,
            True,
        ]:
            return Response(
                {
                    "invalid-invite": "clashing permission levels specified",
                    "invalid-info": f"admin_in was '{request.data['admin_in']}' & viewer_in was '{request.data['viewer_in']}'",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If the data was passed correct, over-write the booleans with the company object
        # If admin_in was True, set the company object for the admin
        if request.data["admin_in"]:
            request.data["admin_in"] = company_obj.id
            request.data["viewer_in"] = None
        # Otherwise, set the company object to the viewer_in field
        else:
            request.data["admin_in"] = None
            request.data["viewer_in"] = company_obj.id

        # Serialize the data
        serializer = self.get_serializer(data=request.data)

        # Check if the information is correct
        if not serializer.is_valid():
            return Response(
                {"invite-error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If admin in company, admin requested, do not send invite
        # If viewer in company, admin requested, set invite
        # If admin in company, viewer requested, do not send invite
        # If viewer in company, viewer requested, do not send invite
        # If not admin or viewer, admin requested, set invite (no dups)
        # If not admin or viewer, viewer requested, check if invite exists, if not set invite (no dups)

        # Get the requested user object to check if they already are in the permissions group
        try:
            invitee_obj = User.objects.get(email=serializer.validated_data["email"])

            existing_admin = company_obj.allowed_admins.filter(
                pk=invitee_obj.pk
            ).exists()
            existing_viewer = company_obj.allowed_viewers.filter(
                pk=invitee_obj.pk
            ).exists()

            if serializer.validated_data["admin_in"]:
                if existing_admin:
                    return Response(
                        {
                            "existing-admin": f"Requested user with email '{serializer.validated_data['email']}' is already set as an admin for '{company_obj.company_name}'",
                            "existing-email": serializer.validated_data["email"],
                        },
                        status=status.HTTP_200_OK,
                    )
                elif existing_viewer:
                    return Response(
                        {
                            "existing-viewer": f"Requested user with email '{serializer.validated_data['email']}' is already set as a viewer for '{company_obj.company_name}'",
                            "existing-email": serializer.validated_data["email"],
                            "no-change": "Viewer status unchanged. Change permission levels in the company parameters.",
                        },
                        status=status.HTTP_200_OK,
                    )

            elif serializer.validated_data["viewer_in"]:
                if existing_admin:
                    return Response(
                        {
                            "existing-admin": f"Requested user with email '{serializer.validated_data['email']}' is already set as an admin for '{company_obj.company_name}'",
                            "existing-email": serializer.validated_data["email"],
                            "no-change": "Admin status unchanged. Change permission levels in the company parameters.",
                        },
                        status=status.HTTP_200_OK,
                    )
                elif existing_viewer:
                    return Response(
                        {
                            "existing-viewer": f"Requested user with email '{serializer.validated_data['email']}' is already set as a viewer for '{company_obj.company_name}'",
                            "existing-email": serializer.validated_data["email"],
                        },
                        status=status.HTTP_200_OK,
                    )

            # If the user exists, but is not assigned to the current company,
            # this will set their permission level
            invite_obj = CompanyInviteList.objects.create(**serializer.validated_data)
            return Response(
                data=CompanyInviteListActiveSerializer(invite_obj).data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(invite_obj),
            )

        except User.DoesNotExist:
            qs_user_invites = self.queryset.filter(
                email=serializer.validated_data["email"]
            )

            # No email user exists, so create the invitation
            if not qs_user_invites.exists():
                invite_obj = CompanyInviteList.objects.create(
                    **serializer.validated_data
                )
                return Response(
                    data=CompanyInviteListActiveSerializer(invite_obj).data,
                    status=status.HTTP_201_CREATED,
                    headers=self.get_success_headers(invite_obj),
                )

            # If a queryset exists, there should be only one entry for the email and company combination.
            # Wrapped in try / except block as a fail-safe for errors
            try:
                invite_obj = self.queryset.get(
                    Q(email=serializer.validated_data["email"]),
                    Q(admin_in=kwargs["pk"]) | Q(viewer_in=kwargs["pk"]),
                )

                invite_obj.admin_in = serializer.validated_data["admin_in"]
                invite_obj.viewer_in = serializer.validated_data["viewer_in"]
                invite_obj.save()

                return Response(
                    data=CompanyInviteListActiveSerializer(invite_obj).data,
                    status=status.HTTP_201_CREATED,
                    headers=self.get_success_headers(invite_obj),
                )

            # This is the fail-safe. Should never reach this.
            except CompanyInviteList.MultipleObjectsReturned:
                # Get all matching invite records
                invite_obj = self.queryset.filter(
                    Q(email=serializer.validated_data["email"]),
                    Q(admin_in=kwargs["pk"]) | Q(viewer_in=kwargs["pk"]),
                )
                # Get a list of all their IDs
                invite_obj_ids = list(invite_obj.values_list("id", flat=True))
                # Remove all records, except for the first record
                invite_obj.filter(id__in=invite_obj_ids[1:]).delete()
                # Reset the variable to the only object left
                invite_obj = invite_obj.first()

                # Save with updated data as standard
                invite_obj.admin_in = serializer.validated_data["admin_in"]
                invite_obj.viewer_in = serializer.validated_data["viewer_in"]
                invite_obj.save()

                return Response(
                    data=CompanyInviteListActiveSerializer(invite_obj).data,
                    status=status.HTTP_201_CREATED,
                    headers=self.get_success_headers(invite_obj),
                )


class CompanyUploadDocumentViewSet(generics.CreateAPIView):
    """
    Handles the upload of several documents at once.
    """

    queryset = Companies.objects.all()
    serializer_class = CompanyUploadDocumentsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, **kwargs):

        # Check that the company exist
        try:
            company_obj = Companies.objects.get(pk=kwargs["pk"])
        # If the company does not exist, return generic response
        except Companies.DoesNotExist:
            return Response(
                data=send_invalid_permission_response(
                    requested_level="company", level_id=kwargs["pk"]
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check that the requesting user is set as an admin for the indicated company
        if not company_obj.allowed_admins.filter(pk=request.user.pk).exists():
            return Response(
                data=send_invalid_permission_response(
                    requested_level="company", level_id=kwargs["pk"]
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Serialize the data
        serializer = self.get_serializer(data=request.data)

        # Check if the information is correct
        if not serializer.is_valid():
            return Response(
                {"document-upload-error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the information behind an atomic transaction
        with transaction.atomic():

            # Save the document and corresponding information
            doc_obj = serializer.save(uploaded_by=request.user)

            # Add that document reference to the company object
            company_obj.documents.add(doc_obj)

        # Set the response headers
        headers = self.get_success_headers(company_obj)

        return Response(
            data=CompanyFullAdminSerializer(company_obj).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
