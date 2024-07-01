from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.schemas.models import Schema
from backend.schemas.tests.factories import (
    SchemaFactory,
)  # Assuming Factory Boy is used


class TestUserViewSet(APITestCase):
    def setUp(self):
        # Create test data
        self.schema1 = SchemaFactory()
        self.schema2 = SchemaFactory()
        self.list_url = reverse("schema-list")
        self.detail_url = lambda pk: reverse("schema-detail", kwargs={"pk": pk})

    def test_list_schemas(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Further checks can be added to verify the content of the response

    def test_retrieve_schema(self):
        response = self.client.get(self.detail_url(self.schema1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify response data matches self.schema1 details

    def test_update_schema(self):
        new_data = {"name": "Updated Name"}  # Assuming 'name' is a field in Schema
        response = self.client.patch(self.detail_url(self.schema1.pk), new_data)
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]
        )
        self.schema1.refresh_from_db()
        self.assertEqual(self.schema1.name, new_data["name"])
