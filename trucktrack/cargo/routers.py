from rest_framework.routers import SimpleRouter

from cargo.views import CargoViewSet, MachineViewSet

cargo = SimpleRouter()
cargo.register(r'cargo', CargoViewSet, basename='cargo')

machine = SimpleRouter()
machine.register(r'machine', MachineViewSet, basename='machine')
