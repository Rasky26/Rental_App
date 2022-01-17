from change_log.models import ChangeLog
from rest_framework import serializers


class ChangeLogCreationSerializer(serializers.ModelSerializer):
    """
    Serializes the creation of the ChangeLog fields
    """

    class Meta:
        models = ChangeLog
        fields = (
            "reference_model",
            "model_id",
            "field_name",
            "previous_value",
            "changed_by",
            "changed_on",
        )
