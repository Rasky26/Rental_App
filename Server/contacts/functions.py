from contacts.models import Addresses


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
