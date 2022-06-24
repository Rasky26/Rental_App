from companies.views import (
    CompanyCreationViewSet,
    CompanyInviteUserViewSet,
    CompanyUploadDocumentViewSet,
)
from django.urls import path

urlpatterns = [
    path("create", CompanyCreationViewSet.as_view(), name="create-company"),
    path("invite/<int:pk>", CompanyInviteUserViewSet.as_view(), name="invite-user"),
    path(
        "<int:pk>/upload-document",
        CompanyUploadDocumentViewSet.as_view(),
        name="upload-company-document",
    ),
]
