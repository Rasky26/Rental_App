from buildings.views import BuildingNoCompanyCreationViewSet
from django.urls import path

urlpatterns = [
    path(
        "no-company/new-building",
        BuildingNoCompanyCreationViewSet.as_view(),
        name="new-building-no-company",
    ),
    # path("<int:pk>/new-building",)
]
