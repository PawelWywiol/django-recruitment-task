from typing import ClassVar

from django.db import models


class User(models.Model):
    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=100)
    initials = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

class UserAddress(models.Model):
    ADDRESS_TYPE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("HOME", "Home"),
        ("INVOICE", "Invoice"),
        ("POST", "Post"),
        ("WORK", "Work"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(max_length=7, choices=ADDRESS_TYPE_CHOICES)
    valid_from = models.DateTimeField()
    post_code = models.CharField(max_length=6)
    city = models.CharField(max_length=60)
    country_code = models.CharField(max_length=3)
    street = models.CharField(max_length=100)
    building_number = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_addresses"
        unique_together = ("user", "address_type", "valid_from")
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"

    def __str__(self) -> str:
        return f"{self.user.email} - {self.address_type} ({self.street} {self.building_number})"
