from accounts.models import User
from django.db import models
from notes.models import Notes, TimeStampMixin

# Create your models here.


class Documents(TimeStampMixin):
    """
    Model used for file storage
    """

    name = models.CharField("Document Name", max_length=255, blank=True)
    document = models.FileField(upload_to="documents")
    uploaded_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, blank=False, null=False
    )
    notes = models.ManyToManyField(
        Notes, related_name="documents_notes_set", blank=True
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ("-updated_at",)

    def __str__(self):
        if self.name:
            return f"{self.updated_at.strftime('%#I:%M %p - %b. %d, %Y')} - {self.name} | {self.document.name}"
        return f"{self.updated_at.strftime('%#I:%M %p - %b. %d, %Y')} - {self.document.name}"


class Images(TimeStampMixin):
    """
    Model used for image storage
    """

    name = models.CharField("Document Name", max_length=255, blank=True)
    image = models.ImageField(upload_to="images")
    uploaded_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, blank=False, null=False
    )
    notes = models.ManyToManyField(Notes, related_name="images_notes_set", blank=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ("-updated_at",)

    def __str__(self):
        if self.name:
            return f"{self.updated_at.strftime('%#I:%M %p - %b. %d, %Y')} - {self.name} | {self.image.name}"
        return (
            f"{self.updated_at.strftime('%#I:%M %p - %b. %d, %Y')} - {self.image.name}"
        )
