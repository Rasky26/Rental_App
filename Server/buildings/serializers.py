from buildings.models import Buildings
from contacts.serializers import AddressSerializer
from documents.serializers import DocumentSerializer, ImageSerializer
from notes.serializers import CreateNoteSerializer, NotesSerializer
from rest_framework import serializers


class BuildingNoCompanyCreationSerializer(serializers.ModelSerializer):
    """
    Building creation serializer
    """

    address = AddressSerializer()
    notes = CreateNoteSerializer(many=True)

    class Meta:
        model = Buildings
        fields = (
            "name",
            "address",
            "build_year",
            "notes",
        )


class BuildingResponseSerializer(serializers.ModelSerializer):
    """
    Returns the building information
    """

    address = AddressSerializer()
    documents = DocumentSerializer(many=True)
    images = ImageSerializer(many=True)
    notes = NotesSerializer(many=True)

    class Meta:
        model = Buildings
        fields = (
            "id",
            "name",
            "address",
            "build_year",
            "documents",
            "images",
            "notes",
        )
