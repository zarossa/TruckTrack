from django.urls import path, include

from cargo.routers import cargo, machine

urlpatterns = [
    path('', include(cargo.urls)),
    path('', include(machine.urls)),
]
