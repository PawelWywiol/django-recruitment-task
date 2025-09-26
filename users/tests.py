from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, UserAddress


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            initials="JD",
            email="john.doe@example.com",
            status="ACTIVE",
        )

    def test_user_creation(self) -> None:
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.status, "ACTIVE")
        self.assertTrue(self.user.created_at)
        self.assertTrue(self.user.updated_at)

    def test_user_str_method(self) -> None:
        expected = "John Doe (john.doe@example.com)"
        self.assertEqual(str(self.user), expected)

    def test_user_status_choices(self) -> None:
        self.assertIn(("ACTIVE", "Active"), User.STATUS_CHOICES)
        self.assertIn(("INACTIVE", "Inactive"), User.STATUS_CHOICES)


class UserAddressModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(first_name="Jane", last_name="Smith", email="jane.smith@example.com")
        self.address = UserAddress.objects.create(
            user=self.user,
            address_type="HOME",
            valid_from=timezone.now(),
            post_code="12345",
            city="Test City",
            country_code="US",
            street="Test Street",
            building_number="123",
        )

    def test_address_creation(self) -> None:
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.address_type, "HOME")
        self.assertEqual(self.address.post_code, "12345")
        self.assertEqual(self.address.city, "Test City")

    def test_address_str_method(self) -> None:
        expected = f"{self.user.email} - HOME (Test Street 123)"
        self.assertEqual(str(self.address), expected)


class UserAPITest(APITestCase):
    def setUp(self) -> None:
        User.objects.all().delete()
        UserAddress.objects.all().delete()

        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "initials": "JD",
            "email": "john.doe@example.com",
            "status": "ACTIVE",
        }
        self.user = User.objects.create(**self.user_data)
        self.list_url = reverse("user-list")
        self.detail_url = reverse("user-detail", kwargs={"pk": self.user.pk})

    def test_create_user(self) -> None:
        new_user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "initials": "JS",
            "email": "jane.smith@example.com",
            "status": "ACTIVE",
        }
        response = self.client.post(self.list_url, new_user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data["email"], "jane.smith@example.com")
        self.assertEqual(response.data["first_name"], "Jane")
        self.assertEqual(response.data["last_name"], "Smith")

    def test_create_user_missing_required_fields(self) -> None:
        invalid_data = {"first_name": "John"}
        response = self.client.post(self.list_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertIn("email", response.data)

    def test_create_user_duplicate_email(self) -> None:
        duplicate_data = {
            "first_name": "Different",
            "last_name": "User",
            "status": "ACTIVE",
            # Same email as existing user
            "email": self.user.email,
        }
        response = self.client.post(self.list_url, duplicate_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_list_users(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if "results" in response.data:
            self.assertEqual(len(response.data["results"]), 1)
            self.assertEqual(response.data["results"][0]["email"], self.user.email)
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["email"], self.user.email)

    def test_retrieve_user(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)

    def test_retrieve_nonexistent_user(self) -> None:
        url = reverse("user-detail", kwargs={"pk": 99999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_put(self) -> None:
        updated_data = {
            "first_name": "Johnny",
            "last_name": "Updated",
            "initials": "JU",
            "email": "john.updated@example.com",
            "status": "INACTIVE",
        }
        response = self.client.put(self.detail_url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Johnny")
        self.assertEqual(self.user.last_name, "Updated")
        self.assertEqual(self.user.email, "john.updated@example.com")
        self.assertEqual(self.user.status, "INACTIVE")

    def test_partial_update_user_patch(self) -> None:
        patch_data = {"first_name": "Updated John"}
        response = self.client.patch(self.detail_url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")

    def test_update_user_duplicate_email(self) -> None:
        self._other_user = User.objects.create(first_name="Other", last_name="User", email="other@example.com")

        updated_data = {
            "first_name": "John",
            "last_name": "Doe",
            "status": "ACTIVE",
            # Trying to use other user's email
            "email": "other@example.com",
        }
        response = self.client.put(self.detail_url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_delete_user(self) -> None:
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_delete_nonexistent_user(self) -> None:
        url = reverse("user-detail", kwargs={"pk": 99999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_with_addresses_serialization(self) -> None:
        self._address = UserAddress.objects.create(
            user=self.user,
            address_type="HOME",
            valid_from=timezone.now(),
            post_code="12345",
            city="Test City",
            country_code="US",
            street="Test Street",
            building_number="123",
        )

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["addresses"]), 1)
        self.assertEqual(response.data["addresses"][0]["address_type"], "HOME")
        self.assertEqual(response.data["addresses"][0]["city"], "Test City")

    def test_invalid_status_value(self) -> None:
        invalid_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "status": "INVALID_STATUS",
        }
        response = self.client.post(self.list_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_empty_email_validation(self) -> None:
        invalid_data = {"first_name": "Test", "last_name": "User", "email": "", "status": "ACTIVE"}
        response = self.client.post(self.list_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_invalid_email_format(self) -> None:
        invalid_data = {"first_name": "Test", "last_name": "User", "email": "invalid-email", "status": "ACTIVE"}
        response = self.client.post(self.list_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_user_creation_with_optional_fields(self) -> None:
        minimal_data = {"last_name": "MinimalUser", "email": "minimal@example.com"}
        response = self.client.post(self.list_url, minimal_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], "")
        self.assertEqual(response.data["initials"], "")
        self.assertEqual(response.data["status"], "ACTIVE")

    def test_read_only_fields(self) -> None:
        update_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated@example.com",
            "status": "ACTIVE",
            # Trying to update read-only field
            "id": 99999,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-01T00:00:00Z",
        }
        original_id = self.user.id
        original_created_at = self.user.created_at

        response = self.client.put(self.detail_url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.id, original_id)
        self.assertEqual(self.user.created_at, original_created_at)
