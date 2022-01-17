from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    pass

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = (
            "last_name",
            "first_name",
        )

    def __str__(self):
        if (not self.first_name) and (not self.last_name):
            return f"{self.username}"
        elif not self.first_name:
            return f"{self.username} | {self.last_name}"
        elif not self.last_name:
            return f"{self.username} | {self.first_name}"
        return f"{self.username} | {self.first_name} {self.last_name}"

    def display_name(self):
        """
        Returns a name string
        """
        return self.__str__()


# class EmailConfirmation(models.Model):
#     """
#     Confirms the user registration within a set time-frame
#     """

#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="user_confirmation_set"
#     )
#     confirmation_code = models.CharField(max_length=6, blank=False)
#     timestamp = models.DateTimeField(auto_now_add=timezone.now)

#     @property
#     def code_timed_out(self):
#         """
#         Gives 6-hours for the User to confirm the code
#         """
#         return self.timestamp + timedelta(hours=6) > timezone.now()
