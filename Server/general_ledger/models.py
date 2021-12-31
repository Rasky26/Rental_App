from django.db import models
from notes.models import Notes, TimeStampMixin

# Create your models here.


class GeneralLedgerCodes(TimeStampMixin):
    """
    Model for storing the general ledger accounts.
    """

    name = models.CharField("General Ledger Name", max_length=127)
    code = models.CharField("General Ledger Code", max_length=15, blank=True)
    description = models.CharField(max_length=1023, blank=True)
    notes = models.ManyToManyField(
        Notes, related_name="general_ledger_notes_set", blank=True
    )

    class Meta:
        verbose_name = "General Ledger Code"
        verbose_name_plural = "General Ledger Codes"
        ordering = (
            "name",
            "code",
        )

    def __str__(self):
        if self.code:
            return f"{self.name} | {self.code}"
        return f"{self.name}"
