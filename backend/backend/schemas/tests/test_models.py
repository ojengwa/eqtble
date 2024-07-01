from datetime import date
from django.db.models import QuerySet
from backend.schemas.models import Schema


def test_schema_soft_delete():
    schema = Schema(name="Test Schema", description="Test Description")
    schema.save()
    schema.delete()
    schema.refresh_from_db()
    assert schema.deleted is True
    assert schema.deleted_at == date.today()
    assert Schema.objects.filter(pk=schema.pk).exists()


def test_schema_full_delete():
    schema = Schema(name="Test Schema Full", description="Test Description Full")
    schema.save()
    schema.delete(full=True)
    assert not Schema.objects.filter(pk=schema.pk).exists()


def test_schema_delete_all_soft():
    parent_schema = Schema(name="Parent Schema", description="Parent Description")
    parent_schema.save()
    for _ in range(3):
        Schema(
            marker=parent_schema.marker, name="Child Schema", description="Child Description"
        ).save()
    parent_schema.delete_all()
    related_schemas = Schema.objects.filter(marker=parent_schema.marker)
    assert all(schema.deleted for schema in related_schemas)
    assert all(schema.deleted_at == date.today() for schema in related_schemas)


def test_schema_delete_all_full():
    parent_schema = Schema(
        name="Parent Schema Full", description="Parent Description Full"
    )
    parent_schema.save()
    for _ in range(3):
        Schema(
            marker=parent_schema.marker,
            name="Child Schema Full",
            description="Child Description Full",
        ).save()
    parent_schema.delete_all(full=True)
    related_schemas = Schema.objects.filter(marker=parent_schema.marker)
    assert not related_schemas.exists()
