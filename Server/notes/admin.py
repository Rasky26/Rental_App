from django.contrib import admin
from .models import Notes


# Register your models here.


class TimeStampFullMixinAdmin(admin.ModelAdmin):
    """
    Add this class to admin.site.register to include the
    'created_at' and the 'updated_at' fields to your admin
    panel.
    """

    readonly_fields = (
        "created_at",
        "updated_at",
    )


class TimeStampCreationMixinAdmin(admin.ModelAdmin):
    """
    Add this class to admin.site.register to include the
    'created_at' field to your admin panel.
    """

    readonly_fields = ("created_at",)


admin.site.register(Notes, TimeStampCreationMixinAdmin)
