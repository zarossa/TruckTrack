import csv
import random

from django.core.management.base import BaseCommand

from cargo.models import State, City, Location, Machine


class Command(BaseCommand):
    help = 'Import data from CSV and create 20 Machine instances'

    def handle(self, *args, **options):
        if not Location.objects.exists():
            with open('uszips.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    state, _ = State.objects.get_or_create(code=row['state_id'], name=row['state_name'])
                    city, _ = City.objects.get_or_create(city=row['city'], state=state)
                    Location.objects.create(city=city, postal_code=row['zip'], latitude=row['lat'],
                                            longitude=row['lng'])

        if not Machine.objects.exists():
            all_locations = Location.objects.all()

            for i in range(20):
                random_location = random.choice(all_locations)
                random_load_capacity = random.randint(1, 1000)
                Machine.objects.create(
                    number=f'{i+1:04d}A',
                    location=random_location,
                    load_capacity=random_load_capacity
                )
