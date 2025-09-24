from typing import ClassVar

from django.contrib import admin

from .models import User, UserAddress


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 0
    fields = ("address_type", "valid_from", "street", "building_number", "post_code", "city", "country_code")
    readonly_fields = ("created_at", "updated_at")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "status", "created_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("first_name", "last_name", "email", "initials")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": ("first_name", "last_name", "initials", "email", "status"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    inlines: ClassVar[list[UserAddressInline]] = [UserAddressInline]
    ordering = ("-created_at",)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "address_type", "street", "building_number", "city", "country_code", "valid_from")
    list_filter = ("address_type", "country_code", "valid_from", "created_at")
    search_fields = ("user__first_name", "user__last_name", "user__email", "street", "city")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": ("user", "address_type", "valid_from"),
            },
        ),
        (
            "Address Details",
            {
                "fields": ("street", "building_number", "post_code", "city", "country_code"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    ordering = ("-created_at",)
