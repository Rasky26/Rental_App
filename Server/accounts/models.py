from django.contrib.auth.models import AbstractUser

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
