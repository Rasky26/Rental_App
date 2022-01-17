from django.urls import path
from notes.views import GetAndEditNoteViewset

urlpatterns = [
    path("<int:pk>/update", GetAndEditNoteViewset.as_view(), name="update-note")
]
