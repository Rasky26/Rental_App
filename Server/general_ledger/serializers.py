from general_ledger.models import GeneralLedgerCodes
from notes.serializers import NotesNewlyCreatedSerializer
from rest_framework import serializers


class GeneralLedgerNoCodeSerializer(serializers.ModelSerializer):
    """
    Serializes the general ledger table
    """

    notes = NotesNewlyCreatedSerializer

    class Meta:
        model = GeneralLedgerCodes
        fields = (
            "id",
            "name",
            "code",
            "description",
            "notes",
        )
