from accounts.serializers import UserReturnStringSerializer
from notes.models import Notes
from rest_framework import serializers

# Create serializer classes here


class CreateNoteSerializer(serializers.ModelSerializer):
    """
    Only needs the singualar 'note' field for creation
    """

    class Meta:
        model = Notes
        fields = ("note",)


class NotesNewlyCreatedSerializer(serializers.ModelSerializer):
    """
    Serializes a newly created note object
    """

    user = UserReturnStringSerializer()

    class Meta:
        model = Notes
        fields = (
            "id",
            "note",
            "user",
            "created_at",
        )
