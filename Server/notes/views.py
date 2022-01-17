from notes.models import Notes
from notes.serializers import CreateNoteSerializer, NotesSerializer
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
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    # def update(self, request, **kwargs):
    # def update(self, request, **kwargs):
    #     """
    #     Check for difference from existing note to request note. Save any differences to the change log table
    #     """
    #     # Serialize the data
    #     serializer = self.get_serializer(data=request.data)

    #     if not serializer.is_valid():
    #         return Response({"bad": "bad serializer"})

    #     print(request.data)
    #     print(kwargs, "!!!!!!!!!")

    #     print(request.data.keys())

    #     existing_note = Notes.objects.get(id=kwargs["pk"])

    #     print(existing_note)

    #     return Response({})

    # if existing_note.user != self.request.user:
    #     return Response(
    #         {"incorrect-user": "Can not edit different user's note."},
    #         status=status.HTTP_401_UNAUTHORIZED,
    #     )

    # If the note already has an edited note linked to it, return error response
    # if existing_note.changed_to:
    #     return Response(
    #         {
    #             "edit-exist": "Note already has edits applied. Can not edit an edited note."
    #         },
    #         status=status.HTTP_304_NOT_MODIFIED,
    #     )

    # serializer = self.get_serializer(data=request.data)
    # serializer.is_valid(raise_exceptions=True)
    # new_note = serializer.save(user=self.request.user)
