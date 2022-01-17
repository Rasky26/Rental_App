from accounts.models import User
from companies.models import Companies, PackageExtensionsMixin
from contacts.models import Addresses, Contacts
from documents.models import Documents, Images
from django.db import models
from general_ledger.models import GeneralLedgerCodes
from notes.models import Notes, TimeStampMixin

# Create your models here.


class Buildings(PackageExtensionsMixin, TimeStampMixin):
    """
    Hold information related to an individual building which may contain one to several units
    """

    company = models.ForeignKey(
        Companies, related_name="buildings_company_set", on_delete=models.RESTRICT
    )
    name = models.CharField(max_length=255, blank=False)
    address = models.ForeignKey(
        Addresses,
        related_name="building_address_set",
        on_delete=models.SET_NULL,
        null=True,
    )
    gl_code = models.ForeignKey(
        GeneralLedgerCodes,
        related_name="building_gl_codes_set",
        on_delete=models.CASCADE,
    )
    build_year = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    allowed_admins = models.ManyToManyField(
        User, related_name="building_user_set", blank=True
    )
    allowed_viewers = models.ManyToManyField(
        User, related_name="building_viewers_set", blank=True
    )
    documents = models.ManyToManyField(
        Documents, related_name="building_documents_set", blank=True
    )
    images = models.ManyToManyField(
        Images, related_name="building_images_set", blank=True
    )
    notes = models.ManyToManyField(Notes, related_name="building_notes_set", blank=True)

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"
        ordering = (
            "company",
            "name",
        )

    def __str__(self):
        return f"{self.company.company_name} | {self.name}"
