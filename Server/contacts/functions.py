from contacts.models import Addresses, Contacts


def populate_address_dict(address):
    """
    Takes in either an address dict or None and populates any missing fields as blanks.

    Used to quickly serialize and validate an Address object
    """
    # Get the fields from the address model
    address_fields = Addresses._meta.fields

    # If the field is set to None, create a blank Address dict
    if address is None:
        address = {}

    # Otherwise, if a field is missing from the provided address
    # dict, add it with a value of blank
    for field in address_fields:
        # Get the field name as a string
        field_str = str(field).split(".")[-1]
        # Skip the 'id' value
        if field_str == "id":
            continue
        # If a field is missing, add a blank value to the dict
        if field_str not in address:
            address[field_str] = ""
        # Otherwise, make sure the supplied address gets extra spaces removed
        else:
            address[field_str] = " ".join(address[field_str].split())

    return address


def populate_contact_dict(contact):
    """
    Takes in either an contact dict or None and populates any missing fields as blanks.

    Used to quickly serialize and validate an Contact object
    """
    # Get the fields from the contact model
    contact_fields = Contacts._meta.fields

    # If the field is set to None, create a blank Contact dict
    if contact is None:
        contact = {}

    # Otherwise, if a field is missing from the provided contact
    # dict, add it with a value of blank
    for field in contact_fields:
        # Get the field name as a string
        field_str = str(field).split(".")[-1]
        # Skip the 'id' value
        if field_str in ["id", "notes"]:
            continue
        # If a field is missing, add a blank value to the dict
        if field_str not in contact:
            contact[field_str] = ""
        # Set the phone record to be a string of numbers only
        elif field_str.startswith("phone"):
            contact[field_str] = "".join(n for n in contact[field_str] if n.isdigit())
        # Otherwise, make sure the supplied contact gets extra spaces removed
        else:
            contact[field_str] = " ".join(contact[field_str].split())

    return contact
