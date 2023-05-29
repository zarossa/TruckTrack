import random
from geopy import distance

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Cargo, Location, Machine


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


class CargoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id']


class CargoListSerializer(CargoLocationSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'pick_up', 'delivery']


class CargoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'weight', 'description']


class CargoRetrieveSerializer(CargoLocationSerializer):
    pick_up_postal = serializers.IntegerField(write_only=True)
    delivery_postal = serializers.IntegerField(write_only=True)
    machine_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up', 'pick_up_postal', 'delivery', 'delivery_postal', 'weight', 'description',
                  'machine_list']

    @staticmethod
    def get_machine_list(obj):
        cargo_location = obj.pick_up
        machine_list = []
        for machine in Machine.objects.all():
            machine_location = machine.location
            if machine_location:
                cargo_point = (cargo_location.latitude, cargo_location.longitude)
                machine_point = (machine_location.latitude, machine_location.longitude)
                dist = distance.distance(cargo_point, machine_point).miles
                machine_list.append({'number': machine.number, 'distance': dist})
        return machine_list

    def validate(self, attrs):
        pick_up_postal = attrs.pop('pick_up_postal')
        delivery_postal = attrs.pop('delivery_postal')

        attrs['pick_up'] = get_location(pick_up_postal, 'pick_up_postal')
        attrs['delivery'] = get_location(delivery_postal, 'delivery_postal')

        return attrs


class MachineSerializer(serializers.ModelSerializer):
    location_postal = serializers.IntegerField(write_only=True)

    class Meta:
        model = Machine
        fields = ['id', 'location_postal']

    def validate(self, attrs):
        location_postal = attrs.pop('location_postal')
        location = get_location(location_postal, 'location_postal')

        attrs['location'] = location
        return attrs


class MachineCreateSerializer(MachineSerializer):
    location_postal = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Machine
        fields = ['id', 'number', 'location_postal', 'load_capacity']

    def validate(self, attrs):
        location_postal = attrs.pop('location_postal', None)
        if location_postal is not None:
            location = get_location(location_postal, 'location_postal')
        else:
            locations = Location.objects.all()
            if locations.exists():
                location = random.choice(locations)
            else:
                raise serializers.ValidationError("No locations available.")

        attrs['location'] = location
        return attrs


def get_location(postal_code: int, location_type: str):
    try:
        return Location.objects.get(postal_code=postal_code)
    except ObjectDoesNotExist:
        raise serializers.ValidationError({location_type: ["Location does not exist for this postal code."]})
