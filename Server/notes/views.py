from notes.models import Notes
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from serializers import CreateNoteSerializer

# Create your views here.


class EditNoteViewset(CreateAPIView):
    """
    Note deletion is not allowed.

    Instead, point the edited note back to the previous
    (original) note. Use the field 'changed_to' to
    point to the edited note.
    """

    queryset = Notes.objects.all()
    serializer_class = CreateNoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, **kwargs):
        """
        Get the existing note and ensure it exists in the database.
        If it does, create the new note and link the existing note
        with that new updated note.
        """
        existing_note = Notes.objects.get(kwargs["note"])

        if existing_note.user != self.request.user:
            return Response(
                {"incorrect-user": "Can not edit different user's note."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # If the note already has an edited note linked to it, return error response
        if existing_note.changed_to:
            return Response(
                {
                    "edit-exist": "Note already has edits applied. Can not edit an edited note."
                },
                status=status.HTTP_304_NOT_MODIFIED,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exceptions=True)
        new_note = serializer.save(user=self.request.user)
