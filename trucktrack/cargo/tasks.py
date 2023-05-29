import random

from proj.celery import app
from .models import Machine, Location


@app.task
def update_machine_location():
    machines = Machine.objects.all()
    locations = Location.objects.all()
    if locations.exists():
        for machine in machines:
            location = random.choice(locations)
            machine.location = location
            machine.save()
