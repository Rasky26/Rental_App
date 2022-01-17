from accounts.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class ChangeLog(models.Model):
    """
    Used as the central storage for objects that are updated.
    """

    class ModelList(models.TextChoices):
        """
        List of models in database to validate against
        """

        # accounts.models
        USER = "User"
        # companies.models
        COMPANIES = "Companies"
        COMPANY_INVITE_LIST = "CompanyInviteList"
        # contacts.models
        ADDRESSES = "Addresses"
        CONTACTS = "Contacts"
        # documents.models
        DOCUMENTS = "Documents"
        IMAGES = "Images"
        # general_ledger.models
        GENERAL_LEDGER_CODES = "GeneralLedgerCodes"
        # notes.models
        NOTES = "Notes"
        # DEFAULT - INVALID SELECTION
        INVALID = "---"

    reference_model = models.CharField(
        "Model Name",
        max_length=127,
        choices=ModelList.choices,
        default=ModelList.INVALID,
    )
    model_id = models.BigIntegerField(
        "Reference Model ID Value", blank=False, null=False
    )
    field_name = models.CharField("Model Field Name", max_length=127, blank=False)
    previous_value = models.TextField("Previously Stored Value")
    previous_value_type = models.CharField(
        "Field Type __name__", max_length=7, blank=False
    )
    previous_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    changed_on = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        verbose_name = "Change Log"
        verbose_name_plural = "Changes Log"
        ordering = ("-changed_on",)

    def __str__(self):
        return f"{self.changed_on.strftime('%#I:%M %p - %b. %d, %Y')} | table: '{self.reference_model}: PK {self.model_id}' - {self.previous_value_type}({self.previous_value[:63]}) | Previous author: {self.previous_user}"
