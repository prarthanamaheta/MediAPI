
from rest_framework import generics

from MediOrganisation.models import Organisation
from MediOrganisation.serializers import OrganisationSerializer


class OrganisationList(generics.ListAPIView):

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

