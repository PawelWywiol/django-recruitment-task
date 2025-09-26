from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User, UserAddress
from .serializers import UserAddressSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Users with full CRUD operations.

    This ViewSet provides:
    - GET /api/users/ - List all users
    - POST /api/users/ - Create a new user
    - GET /api/users/{id}/ - Retrieve a specific user
    - PUT /api/users/{id}/ - Update a user (full update)
    - PATCH /api/users/{id}/ - Partially update a user
    - DELETE /api/users/{id}/ - Delete a user
    """

    queryset = User.objects.all().prefetch_related("addresses")
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="List all users",
        operation_description="Retrieve a list of all users with their addresses",
        responses={
            200: UserSerializer(many=True),
        },
    )
    def list(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new user",
        operation_description="Create a new user with the provided data",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Bad Request - Validation errors",
        },
    )
    def create(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a user",
        operation_description="Retrieve a specific user by ID with their addresses",
        responses={
            200: UserSerializer,
            404: "User not found",
        },
    )
    def retrieve(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a user",
        operation_description="Update all fields of a user",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Bad Request - Validation errors",
            404: "User not found",
        },
    )
    def update(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a user",
        operation_description="Update specific fields of a user",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Bad Request - Validation errors",
            404: "User not found",
        },
    )
    def partial_update(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a user",
        operation_description="Delete a user and all associated addresses",
        responses={
            204: "User successfully deleted",
            404: "User not found",
        },
    )
    def destroy(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().destroy(request, *args, **kwargs)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing User Addresses with full CRUD operations.

    This ViewSet provides:
    - GET /api/users/{id}/address/ - List addresses for a specific user
    - POST /api/users/{id}/address/ - Create a new address for a user
    - GET /api/users/{id}/address/{address_id}/ - Retrieve a specific user address
    - PUT /api/users/{id}/address/{address_id}/ - Update a user address (full update)
    - PATCH /api/users/{id}/address/{address_id}/ - Partially update a user address
    - DELETE /api/users/{id}/address/{address_id}/ - Delete a user address
    """

    serializer_class = UserAddressSerializer

    def get_queryset(self) -> QuerySet[UserAddress]:
        user_id = self.kwargs.get("id")
        return UserAddress.objects.filter(user_id=user_id).select_related("user")

    def perform_create(self, serializer: UserAddressSerializer) -> None:
        user_id = self.kwargs.get("id")
        serializer.save(user_id=user_id)

    def get_object(self) -> UserAddress:
        user_id = self.kwargs.get("id")
        address_id = self.kwargs.get("address_id")
        return get_object_or_404(UserAddress, user_id=user_id, id=address_id)

    @swagger_auto_schema(
        operation_summary="List all user addresses",
        operation_description="Retrieve a list of all user addresses",
        responses={
            200: UserAddressSerializer(many=True),
        },
    )
    def list(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new user address",
        operation_description="Create a new user address with the provided data",
        request_body=UserAddressSerializer,
        responses={
            201: UserAddressSerializer,
            400: "Bad Request - Validation errors",
        },
    )
    def create(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a user address",
        operation_description="Retrieve a specific user address by ID",
        responses={
            200: UserAddressSerializer,
            404: "User address not found",
        },
    )
    def retrieve(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a user address",
        operation_description="Update all fields of a user address",
        request_body=UserAddressSerializer,
        responses={
            200: UserAddressSerializer,
            400: "Bad Request - Validation errors",
            404: "User address not found",
        },
    )
    def update(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a user address",
        operation_description="Update specific fields of a user address",
        request_body=UserAddressSerializer,
        responses={
            200: UserAddressSerializer,
            400: "Bad Request - Validation errors",
            404: "User address not found",
        },
    )
    def partial_update(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a user address",
        operation_description="Delete a user address",
        responses={
            204: "User address successfully deleted",
            404: "User address not found",
        },
    )
    def destroy(self, request: Request, *args: object, **kwargs: dict) -> Response:
        return super().destroy(request, *args, **kwargs)
