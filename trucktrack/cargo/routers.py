from rest_framework.routers import SimpleRouter

from cargo.views import CargoViewSet

cargo = SimpleRouter()
cargo.register(r'cargo', CargoViewSet, basename='cargo')
