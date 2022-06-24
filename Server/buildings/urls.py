from buildings.views import (
    BuildingCreationWithCompanyViewSet,
    BuildingNoCompanyCreationViewSet,
    BuildingUpdateViewSet,
)
from django.urls import path

urlpatterns = [
    path(
        "no-company/new-building",
        BuildingNoCompanyCreationViewSet.as_view(),
        name="new-building-no-company",
    ),
    path(
        "<int:pk>/new-building",
        BuildingCreationWithCompanyViewSet.as_view(),
        name="new-building-with-company",
    ),
    path(
        "<int:pk>/update",
        BuildingUpdateViewSet.as_view(),
        name="retrieve-and-update-building",
    ),
]
