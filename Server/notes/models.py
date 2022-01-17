from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.


class TimeStampMixin(models.Model):
    """
    Sets both the creation time stamp and any update
    time stamps. Can inherit into any model.
    """

    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        abstract = True


class Notes(TimeStampMixin):
    """
    Master log of notes. Accessed by various models
    via ManyToMany relationships.
    """

    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = (
            "-created_at",
            "note",
        )

    def __str__(self):
        if len(self.note) > 31:
            return f'{self.created_at.strftime("%#I:%M %p - %b. %d, %Y")} - {self.note[:31]}...'
        return f'{self.created_at.strftime("%#I:%M %p - %b. %d, %Y")} - {self.note}'
