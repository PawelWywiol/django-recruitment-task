from django.db import connection
from django.db.utils import DatabaseError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@swagger_auto_schema(
    method="get",
    operation_summary="Health check",
    operation_description="Check the health status of the application and database connectivity",
    responses={
        200: "Application is healthy",
        503: "Application is unhealthy",
    },
)
@api_view(["GET"])
def health_check(request: Request) -> Response:  # noqa: ARG001
    """
    Health check endpoint that verifies database connectivity.

    Returns:
        Response with status "UP" or "DOWN" and detailed checks
    """
    checks = []
    overall_status = "UP"
    response_status = status.HTTP_200_OK

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        db_status = "UP"
    except DatabaseError:
        db_status = "DOWN"
        overall_status = "DOWN"
        response_status = status.HTTP_503_SERVICE_UNAVAILABLE

    checks.append(
        {
            "name": "databaseReady",
            "status": db_status,
        },
    )

    return Response(
        {
            "status": overall_status,
            "checks": checks,
        },
        status=response_status,
    )
