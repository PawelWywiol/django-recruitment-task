
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


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
