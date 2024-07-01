import pytest
from backend.schemas.api.serializers import SchemaSerializer
from backend.schemas.models import Schema


def test_schema_serializer_meta_model():
    assert SchemaSerializer.Meta.model == Schema, "The model should be Schema."


def test_schema_serializer_meta_fields():
    expected_fields = ["name", "url"]
    assert (
        SchemaSerializer.Meta.fields == expected_fields
    ), "The fields should exactly match ['name', 'url']."


def test_schema_serializer_meta_extra_kwargs():
    expected_extra_kwargs = {
        "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
    }
    assert (
        SchemaSerializer.Meta.extra_kwargs == expected_extra_kwargs
    ), "The extra_kwargs for 'url' should match the expected dictionary."
