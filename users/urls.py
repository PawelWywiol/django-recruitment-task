from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserAddressViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/users/<int:id>/address/", UserAddressViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="user-address-list"),
    path("api/users/<int:id>/address/<int:address_id>/", UserAddressViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }), name="user-address-detail"),
]
