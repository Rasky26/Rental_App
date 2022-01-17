from accounts.serializers import UserReturnStringSerializer
from documents.models import Documents, Images
from notes.serializers import NoteCreateSerializer, NotesSerializer
from rest_framework import serializers


class DocumentCreationSerializer(serializers.ModelSerializer):
    """
    Serializes an uploaded file to be saved
    """

    notes = NoteCreateSerializer(many=True)

    class Meta:
        model = Documents
        fields = (
            "name",
            "document",
            "uploaded_by",
            "notes",
        )


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializes an existing document object.
    """

    uploaded_by = UserReturnStringSerializer(read_only=True)
    notes = NotesSerializer(many=True, read_only=True)

    class Meta:
        model = Documents
        fields = (
            "id",
            "name",
            "document",
            "uploaded_by",
            "notes",
            "created_at",
        )


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializes an existing image object.
    """

    uploaded_by = UserReturnStringSerializer(read_only=True)
    notes = NotesSerializer(many=True, read_only=True)

    class Meta:
        model = Images
        fields = (
            "id",
            "name",
            "image",
            "uploaded_by",
            "notes",
            "created_at",
        )
