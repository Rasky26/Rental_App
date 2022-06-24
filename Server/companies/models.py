from datetime import timedelta

from django.db.models.fields import related
from documents.models import Documents, Images
from django.db import models
from django.utils import timezone
from accounts.models import User
from contacts.models import Addresses, Contacts
from general_ledger.models import GeneralLedgerCodes
from notes.models import Notes, TimeStampMixin

# Create your models here.


class PackageExtensionsMixin(models.Model):
    """
    Class that tracks package extensions.

    Abstract class, applied where necessary.
    """

    accounts_payable_extension = models.BooleanField(
        "Accounts Payable Package Extension", default=False
    )
    accounts_receivable_extension = models.BooleanField(
        "Accounts Receivable Package Extension", default=False
    )
    maintenance_extension = models.BooleanField(
        "Maintenance Package Extension", default=False
    )

    class Meta:
        abstract = True


class Companies(PackageExtensionsMixin, TimeStampMixin):
    """
    The primary container for all buildings / units.

    Users must be associated with the company before they
    are allowed to access any of its information.

    Additionally, set base information
    """

    business_name = models.CharField(max_length=255, blank=False, default=None)
    legal_name = models.CharField(max_length=255, blank=True)
    business_address = models.ForeignKey(
        Addresses,
        related_name="company_business_address_set",
        on_delete=models.SET_NULL,
        null=True,
    )
    mailing_address = models.ForeignKey(
        Addresses,
        related_name="company_mailing_address_set",
        on_delete=models.SET_NULL,
        null=True,
    )
    contacts = models.ManyToManyField(
        Contacts, related_name="company_contacts_set", blank=True
    )
    gl_code = models.ForeignKey(
        GeneralLedgerCodes,
        related_name="company_gl_codes_set",
        on_delete=models.CASCADE,
    )
    accounts_payable_gl = models.ForeignKey(
        GeneralLedgerCodes,
        related_name="accounts_payable_gl_codes_set",
        on_delete=models.CASCADE,
    )
    accounts_receivable_gl = models.ForeignKey(
        GeneralLedgerCodes,
        related_name="accounts_receivable_gl_codes_set",
        on_delete=models.CASCADE,
    )
    allowed_admins = models.ManyToManyField(
        User, related_name="company_user_set", blank=True
    )
    allowed_viewers = models.ManyToManyField(
        User, related_name="company_viewers_set", blank=True
    )
    documents = models.ManyToManyField(
        Documents, related_name="company_documents_set", blank=True
    )
    images = models.ManyToManyField(
        Images, related_name="company_images_set", blank=True
    )
    notes = models.ManyToManyField(Notes, related_name="company_notes_set", blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ("business_name",)

    def __str__(self):
        if self.legal_name:
            return f"{self.business_name} | {self.legal_name}"
        return f"{self.business_name}"

    @property
    def company_name(self):
        """
        Returns the company's name and legal name if available
        """
        return self.__str__()


class CompanyInviteList(TimeStampMixin):
    """
    Table to hold emailed invites for specific companies to various users and their expected roles
    """

    email = models.EmailField("Invited user")
    admin_in = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        related_name="invite_admin_company_set",
        blank=True,
        null=True,
    )
    viewer_in = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        related_name="invite_viewer_company_set",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Company Invite List"
        verbose_name_plural = "Company Invites List"
        ordering = (
            "-updated_at",
            "email",
        )
        # https://stackoverflow.com/a/66860132
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_admin_in_or_viewer_in",
                check=(
                    models.Q(admin_in__isnull=True, viewer_in__isnull=False)
                    | models.Q(admin_in__isnull=False, viewer_in__isnull=True)
                ),
            )
        ]
        unique_together = (
            "email",
            "admin_in",
            "viewer_in",
        )

    def __str__(self):
        if self.admin_in:
            return f"{self.email} - Admin Invitation - Valid until: {(self.updated_at + timedelta(days=7)).strftime('%b. %d, %Y - %I:%M %p UTC')}"
        return f"{self.email} - Viewer Invitation - Valid until: {(self.updated_at + timedelta(days=7)).strftime('%b. %d, %Y - %I:%M %p UTC')}"

    @property
    def timeout(self):
        """
        Checks if the invite has is no longer valid. Invite links are valid for seven (7) days.

        Uses the 'updated_at' field, which reflects when the latest changes were made.
        """
        return self.updated_at + timedelta(days=7) < timezone.now()
