from django.urls import path
from notes.views import GetAndEditNoteViewset

urlpatterns = [path("<int:pk>", GetAndEditNoteViewset.as_view(), name="update-note")]
