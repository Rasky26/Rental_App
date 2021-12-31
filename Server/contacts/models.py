from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Addresses(models.Model):
    """
    Central model for storing addresses.
    """

    class StateList(models.TextChoices):
        ALABAMA = "AL", "Alabama"
        ALASKA = "AK", "Alaska"
        ARIZONA = "AZ", "Arizona"
        ARKANSAS = "AR", "Arkansas"
        CALIFORNIA = "CA", "California"
        COLORADO = "CO", "Colorado"
        CONNECTICUT = "CT", "Connecticut"
        DELAWARE = "DE", "Delaware"
        DISTRICT_OF_COLUMBIA = "DC", "District of Columbia"
        FLORDIA = "FL", "Florida"
        GEORGIA = "GA", "Georgia"
        HAWAII = "HI", "Hawaii"
        IDAHO = "ID", "Idaho"
        ILLINOIS = "IL", "Illinois"
        INDIANA = "IN", "Indiana"
        IOWA = "IA", "Iowa"
        KANSAS = "KS", "Kansas"
        KENTUCKY = "KY", "Kentucky"
        LOUISIANA = "LA", "Louisiana"
        MAINE = "ME", "Maine"
        MARYLAND = "MD", "Maryland"
        MASSACHUSETTS = "MA", "Massachusetts"
        MICHIGAN = "MI", "Michigan"
        MINNESOTA = "MN", "Minnesota"
        MISSISSIPPI = "MS", "Mississippi"
        MISSOURI = "MO", "Missouri"
        MONTANA = "MT", "Montana"
        NEBRASKA = "NE", "Nebraska"
        NEVEDA = "NV", "Nevada"
        NEW_HAMPSHIRE = "NH", "New Hampshire"
        NEW_JERSEY = "NJ", "New Jersey"
        NEW_MEXICO = "NM", "New Mexico"
        NEW_YORK = "NY", "New York"
        NORTH_CAROLINA = "NC", "North Carolina"
        NORTH_DAKOTA = "ND", "North Dakota"
        OHIO = "OH", "Ohio"
        OKLAHOMA = "OK", "Oklahoma"
        OREGON = "OR", "Oregon"
        PENNSYLVANIA = "PA", "Pennsylvania"
        PUERTO_RICO = "PR", "Puerto Rico"
        RHODE_ISLAND = "RI", "Rhode Island"
        SOUTH_CAROLINA = "SC", "South Carolina"
        SOUTH_DAKOTA = "SD", "South Dakota"
        TENNESSEE = "TN", "Tennessee"
        TEXAS = "TX", "Texas"
        UTAH = "UT", "Utah"
        VERMONT = "VT", "Vermont"
        VIRGINIA = "VA", "Virginia"
        WASHINGTON = "WA", "Washington"
        WEST_VIRGINIA = "WV", "West Virginia"
        WISCONSIN = "WI", "Wisconsin"
        WYOMING = "WY", "Wyoming"

    address1 = models.CharField("Address 1", max_length=255, blank=True)
    address2 = models.CharField("Address 2", max_length=63, blank=True)
    city = models.CharField(max_length=127, blank=True)
    state = models.CharField(max_length=2, choices=StateList.choices, blank=True)
    zipcode = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                r"^([0-9]{5})(([-])?[0-9]{0,4})?$",
                message="Invalid zipcode. Format should be XXXXX or XXXXX-XXXX",
                code="invalid-zipcode",
            ),
        ],
    )

    class Meta:
        ordering = (
            "state",
            "city",
            "address1",
        )
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        """
        Returns the address string based on available information.
        """
        # Set empty address_string, and flag for first entry
        address_string = ""
        first = True
        # Enumerate to check against zipcode, which needs no comma
        for step, item in enumerate(
            [self.address1, self.address2, self.city, self.state, self.zipcode]
        ):
            # Add the first item to the address string.
            # Set flag to false
            if item and first:
                address_string = item
                first = False
            # Append additional address fields, except zipcode
            elif item and (step != 4):
                address_string += f", {item}"
            # This should only catch for zipcode
            elif item:
                address_string += f" {item}"

        return address_string


class Contacts(models.Model):
    """
    Contact model, each associated with a specific company.

    This is to preserve contact information to only the
    company that entered them.
    """

    name_prefix = models.CharField(max_length=15, blank=True)
    name_first = models.CharField(max_length=31, blank=True)
    name_middle = models.CharField(max_length=31, blank=True)
    name_last = models.CharField(max_length=31, blank=True)
    name_suffix = models.CharField(max_length=15, blank=True)
    phone_1 = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                r"^\d{10}$",
                message="Invalid phone number. Should be 10 digits",
                code="invalid-phone",
            ),
        ],
    )
    phone_2 = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                r"^\d{10}$",
                message="Invalid phone number. Should be 10 digits",
                code="invalid-phone",
            ),
        ],
    )
    email = models.EmailField(blank=True, null=True, unique=False)

    class Meta:
        ordering = (
            "name_last",
            "name_first",
        )
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.name_first} {self.name_last}"
