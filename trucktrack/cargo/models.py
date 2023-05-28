from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['id']


class State(BaseModel):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"State {self.code}"


class City(BaseModel):
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='cities')

    def __str__(self):
        return f"{self.state}. City {self.city}"


class Location(BaseModel):
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='locations')
    postal_code = models.PositiveIntegerField(unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"ZIP {self.postal_code}. {self.city}"


class Cargo(BaseModel):
    pick_up = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, related_name='pick_up_cargos')
    delivery = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, related_name='delivery_cargos')
    weight = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()


class Machine(BaseModel):
    number_validator = RegexValidator(
        regex=r'^\d{4}[A-Z]$',
        message='Number must be in the format /D/D/D/D/C/ (e.g., 1234G).'
    )

    number = models.CharField(max_length=5, unique=True, validators=[number_validator])
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, related_name='machines')
    load_capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
