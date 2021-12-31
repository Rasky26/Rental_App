from contacts.models import Addresses, Contacts
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializes the Address model
    """

    class Meta:
        model = Addresses
        fields = (
            "id",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
        )


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializes the Contact model
    """

    class Meta:
        model = Contacts
        fields = (
            "id",
            "name_prefix",
            "name_first",
            "name_middle",
            "name_last",
            "name_suffix",
            "phone_1",
            "phone_2",
            "email",
        )
