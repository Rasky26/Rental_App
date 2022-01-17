from buildings.models import Buildings
from buildings.serializers import (
    BuildingNoCompanyCreationSerializer,
    BuildingResponseSerializer,
)
from companies.models import Companies
from contacts.functions import populate_address_dict
from contacts.models import Addresses
from django.db import transaction
from general_ledger.models import GeneralLedgerCodes
from notes.models import Notes
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.


class BuildingNoCompanyCreationViewSet(generics.CreateAPIView):
    """
    Create a new building object
    """

    queryset = Buildings.objects.all()
    serializer_class = BuildingNoCompanyCreationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
        Creates a new building record, and creates a container company name for the saved building name
        """

        # Serialize the data
        serializer = self.get_serializer(data=request.data)

        # Creates a valid address dictionary to be validated against.
        # Accounts for None or missing values
        serializer.initial_data["address"] = populate_address_dict(
            None
            if ("address" not in serializer.initial_data)
            or (serializer.initial_data["address"] is None)
            else serializer.initial_data["address"]
        )

        # Fail-safe to make sure a notes array is included
        if "notes" not in serializer.initial_data:
            serializer.initial_data["notes"] = []

        if not serializer.is_valid():
            return Response(
                {"building-errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Pop out the business address information
        address = serializer.validated_data.pop("address")

        # Pop out company notes if provided
        building_notes = serializer.validated_data.pop("notes")

        # Create a company object built around the entered building name

        # Make all the posts behind an atomic transaction to make sure
        # all entries are successfully made
        with transaction.atomic():

            ###### Company Creation ######
            # Create the encompassing accounts receivable general ledger
            accounts_receivable_gl = GeneralLedgerCodes.objects.create(
                name="Accounts Receivable",
                description=f"Accounts Receivable ledger",
            )

            # Create the encompassing accounts payable general ledger
            accounts_payable_gl = GeneralLedgerCodes.objects.create(
                name="Accounts Payable",
                description=f"Accounts Payable ledger",
            )

            # Create the general ledger account for company expenses
            company_gl_code = GeneralLedgerCodes.objects.create(
                name="Rental Business",
            )

            # Save the company with all the newly created address and company_gl_code objects
            company_obj = Companies.objects.create(
                business_name="Rental Business",
                accounts_payable_gl=accounts_payable_gl,
                accounts_receivable_gl=accounts_receivable_gl,
                gl_code=company_gl_code,
            )

            # Add the current user as an allowed admin
            company_obj.allowed_admins.add(request.user)

            ###### Building Creation ######
            # Check if any address values are present
            if any(address.values()):
                # Save the address
                address_obj = Addresses.objects.create(**address)
            # If all values are blank, save a None value
            else:
                address_obj = None

            # Create the general ledger account for building expenses
            building_gl_code = GeneralLedgerCodes.objects.create(
                name=f"{serializer.validated_data['name']}",
                description=f"{serializer.validated_data['name']} general ledger",
            )

            # Save the building with all the newly created address
            building_obj = serializer.save(
                company=company_obj, address=address_obj, gl_code=building_gl_code
            )

            # If notes are present, loop through each note
            for building_note in building_notes:
                # Assign the user to the note
                building_note["user"] = request.user
                # Create the note with associated user
                building_note_obj = Notes.objects.create(**building_note)
                # Add that note object to the ManyToMany notes field
                building_obj.notes.add(building_note_obj)

        headers = self.get_success_headers(building_obj)

        return Response(
            data=BuildingResponseSerializer(building_obj).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
