from rest_framework import mixins, viewsets

from cargo.models import Cargo
from cargo.serializers import CargoListSerializer, CargoRetrieveSerializer, CargoDeleteSerializer, CargoUpdateSerializer


class CargoViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Cargo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'retrieve':
            return CargoRetrieveSerializer
        elif self.action == 'list':
            return CargoListSerializer
        elif self.action == 'destroy':
            return CargoDeleteSerializer
        elif self.action == 'partial_update' or self.action == 'update':
            return CargoUpdateSerializer
        return super().get_serializer_class()
