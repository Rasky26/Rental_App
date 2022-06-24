from notes.models import Notes
from notes.serializers import NotesSerializer, NoteUpdateSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.


class GetAndEditNoteViewset(RetrieveUpdateAPIView):
    """
    Note deletion is not allowed.

    Instead, point the edited note back to the previous
    (original) note. Use the field 'changed_to' to
    point to the edited note.
    """

    queryset = Notes.objects.all()
    serializer_class = NoteUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, **kwargs):

        try:
            note = Notes.objects.get(pk=kwargs["pk"])
        except Notes.DoesNotExist:
            return Response(
                data={"invalid-note": "unable to access requested note"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().update(request, **kwargs)
