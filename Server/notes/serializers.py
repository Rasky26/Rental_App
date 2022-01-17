from accounts.serializers import UserReturnStringSerializer
from change_log.models import ChangeLog
from django.db import transaction
from notes.models import Notes
from rest_framework import serializers, status
from rest_framework.response import Response

# Create serializer classes here


class NoteCreateSerializer(serializers.ModelSerializer):
    """
    Only needs the singualar 'note' field for creation
    """

    class Meta:
        model = Notes
        fields = ("note",)


class NoteUpdateSerializer(serializers.ModelSerializer):
    """
    Updates a note object.
    All changes are logged in the change_log table.
    """

    class Meta:
        model = Notes
        fields = (
            "id",
            "note",
            "user",
            "updated_at",
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

        if user != instance.user:
            error = {"failed-edit": "Can only edit notes assigned to you"}
            raise serializers.ValidationError(error)

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
                    reference_model="Notes",
                    model_id=instance.id,
                    field_name=field,
                    previous_value=str(old_value),
                    previous_value_type=type(old_value).__name__,
                    previous_user=instance.user,
                )

            validated_data["user"] = user

        return super(NoteUpdateSerializer, self).update(instance, validated_data)


class NotesSerializer(serializers.ModelSerializer):
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
            "updated_at",
        )

    # def update(self, instance, validated_data):
    #     """
    #     Finds all fields that have been updated.
    #     Any updated field is saved to the change log.
    #     """
    #     # Get the user object
    #     user = None
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         user = request.user

    #     with transaction.atomic():

    #         # Existing information is stored on the instance variable.
    #         # New information will be on the validated_data variable.
    #         for field, value in validated_data.items():
    #             new_value = value
    #             old_value = getattr(instance, field)
    #             print(field, new_value, old_value)

    #             # Fail-safe to make sure a change is detected
    #             if new_value == old_value:
    #                 continue

    #             # Save the previous data to the ChangeLog table.
    #             # Each field that was modified will be saved as their own record
    #             ChangeLog.objects.create(
    #                 reference_model="Notes",
    #                 model_id=instance.id,
    #                 field_name=field,
    #                 previous_value=str(old_value),
    #                 previous_value_type=type(old_value).__name__,
    #                 previous_user=instance.user,
    #             )

    #     return super(NotesSerializer, self).update(instance, validated_data)


# def note_full_serializer(note):
#     """
#     Constructs the note serializer structure.

#     'note' is the latest note in the edit chain
#     'previous_notes' is a array of previous notes in the chain
#     """
#     qs = Notes.objects.all()
#     print(note)
