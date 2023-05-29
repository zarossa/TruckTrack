from rest_framework import mixins, viewsets, filters

from cargo.models import Cargo, Machine
from cargo.serializers import CargoListSerializer, CargoRetrieveSerializer, CargoDeleteSerializer, \
    CargoUpdateSerializer, MachineSerializer, MachineCreateSerializer


class CargoViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Cargo.objects.all()
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['weight', 'dist']

    def get_serializer_class(self):
        switch = {
            'create': CargoRetrieveSerializer,
            'retrieve': CargoRetrieveSerializer,
            'list': CargoListSerializer,
            'destroy': CargoDeleteSerializer,
            'partial_update': CargoUpdateSerializer,
            'update': CargoUpdateSerializer,
        }
        return switch.get(self.action)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            weight = self.request.query_params.get('weight', None)
            if weight is not None:
                try:
                    weight = int(weight)
                except ValueError:
                    return queryset.none()
                queryset = queryset.filter(weight=weight)
        return queryset


class MachineViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Machine.objects.all()

    def get_serializer_class(self):
        switch = {
            'create': MachineCreateSerializer,
            'partial_update': MachineSerializer,
            'update': MachineSerializer,
        }
        return switch.get(self.action)
