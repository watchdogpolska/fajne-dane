from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from campaigns.models import InstitutionGroup
from campaigns.serializers import InstitutionGroupSerializer


class InstitutionGroupList(generics.ListAPIView):
    serializer_class = InstitutionGroupSerializer
    permission_classes = (IsAdminUser,)
    queryset = InstitutionGroup.objects.all()


class InstitutionGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstitutionGroupSerializer
    permission_classes = (IsAdminUser,)
    queryset = InstitutionGroup.objects.all()

    def delete(self, request, *args, **kwargs):
        # TODO: check if no documents left
        InstitutionGroup.objects.filter(source_id=kwargs['pk']).delete()
        raise NotImplemented()
