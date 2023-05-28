from django.urls import path, include

from cargo.routers import cargo

urlpatterns = [
    path('', include(cargo.urls)),
]
