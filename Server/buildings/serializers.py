from buildings.models import Buildings
from change_log.models import ChangeLog
from contacts.serializers import AddressSerializer
from django.db import transaction
from documents.serializers import DocumentSerializer, ImageSerializer
from notes.serializers import NoteCreateSerializer, NotesSerializer
from rest_framework import serializers


class BuildingCreationSerializer(serializers.ModelSerializer):
    """
    Building creation serializer
    """

    address = AddressSerializer()
    notes = NoteCreateSerializer(many=True)

    class Meta:
        model = Buildings
        fields = (
            "name",
            "address",
            "build_year",
            "notes",
        )


class BuildingRetrieveAndUpdateSerializer(serializers.ModelSerializer):
    """
    Building creation serializer
    """

    class Meta:
        model = Buildings
        fields = (
            "id",
            "name",
            "build_year",
        )

    def update(self, instance, validated_data):
        """
        Finds all fields that have been updated.
        Any updated field is saved to the change log.
        """
        # Get the current user object
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        # Handle all change logs in a transaction block
        with transaction.atomic():

            # Existing information is stored on the instance variable.
            # New information will be on the validated_data variable.
            for field, value in validated_data.items():
                new_value = value
                old_value = getattr(instance, field)

                # Fail-safe to make sure a change is detected
                if new_value == old_value:
                    continue

                # Save the previous data to the ChangeLog table.
                # Each field that was modified will be saved as their own record
                ChangeLog.objects.create(
                    reference_model="Buildings",
                    model_id=instance.id,
                    field_name=field,
                    previous_value=str(old_value),
                    previous_value_type=type(old_value).__name__,
                    previous_user=user,
                )

            validated_data["user"] = user

        return super(BuildingRetrieveAndUpdateSerializer, self).update(
            instance, validated_data
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
