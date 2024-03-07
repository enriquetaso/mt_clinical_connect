from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Hospital


class HospitalViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hospital = Hospital.objects.create(name="Test Hospital", city="Amsterdam")

    def test_get_all_hospitals(self):
        response = self.client.get("/hospitals/")  # replace with your actual url
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_hospital(self):
        response = self.client.get(
            f"/hospitals/{self.hospital.id}/"
        )  # replace with your actual url
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.hospital.name)

    def test_create_hospital(self):
        data = {"name": "New Hospital", "city": "456 New St"}
        response = self.client.post("/hospitals/", data)  # replace with your actual url
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_hospital(self):
        data = {"name": "Updated Hospital", "city": "789 Updated St"}
        response = self.client.put(
            f"/hospitals/{self.hospital.id}/", data
        )  # replace with your actual url
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Hospital")

    def test_delete_hospital(self):
        response = self.client.delete(
            f"/hospitals/{self.hospital.id}/"
        )  # replace with your actual url
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
