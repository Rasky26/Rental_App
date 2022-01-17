from general_ledger.models import GeneralLedgerCodes
from notes.serializers import NotesSerializer
from rest_framework import serializers


class GeneralLedgerNoCodeSerializer(serializers.ModelSerializer):
    """
    Serializes the general ledger table
    """

    notes = NotesSerializer(many=True)

    class Meta:
        model = GeneralLedgerCodes
        fields = (
            "id",
            "name",
            "code",
            "description",
            "notes",
        )
