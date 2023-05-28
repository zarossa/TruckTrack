from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Cargo, Location


class CargoLocationSerializer(serializers.ModelSerializer):
    pick_up = serializers.SerializerMethodField(read_only=True)
    delivery = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up', 'delivery']

    @staticmethod
    def get_pick_up(obj):
        return str(obj.pick_up) if obj.pick_up else None

    @staticmethod
    def get_delivery(obj):
        return str(obj.delivery) if obj.delivery else None


class CargoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'weight', 'description']


class CargoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id']


class CargoListSerializer(CargoLocationSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'pick_up', 'delivery']


class CargoUpdateSerializer(CargoInfoSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'weight', 'description']


class CargoRetrieveSerializer(CargoInfoSerializer, CargoLocationSerializer):
    pick_up_postal = serializers.IntegerField(write_only=True)
    delivery_postal = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up', 'pick_up_postal', 'delivery', 'delivery_postal', 'weight', 'description']

    @staticmethod
    def get_location(postal_code: int, location_type: str):
        try:
            return Location.objects.get(postal_code=postal_code)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({location_type: ["Location does not exist for this postal code."]})

    def validate(self, attrs):
        pick_up_postal = attrs.pop('pick_up_postal')
        delivery_postal = attrs.pop('delivery_postal')

        attrs['pick_up'] = self.get_location(pick_up_postal, 'pick_up_postal')
        attrs['delivery'] = self.get_location(delivery_postal, 'delivery_postal')

        return attrs
