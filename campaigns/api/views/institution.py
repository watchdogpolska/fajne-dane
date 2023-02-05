from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from campaigns.models import Institution
from campaigns.serializers import InstitutionSerializer


class InstitutionList(generics.ListAPIView):
    serializer_class = InstitutionSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        return Institution.objects.filter(group_id=group_id)


class InstitutionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstitutionSerializer
    permission_classes = (IsAdminUser,)
    queryset = Institution.objects.all()

    def delete(self, request, *args, **kwargs):
        # TODO: check if no documents left
        Institution.objects.filter(source_id=kwargs['pk']).delete()
        raise NotImplemented()
