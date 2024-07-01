from rest_framework import serializers

from backend.schemas.models import Schema
from .validators import FileValidator


class SchemaSerializer(serializers.ModelSerializer[Schema]):
    file = serializers.FileField(validators=[FileValidator()])

    class Meta:
        model = Schema
        exclude = ["marker", "deleted"]
        read_only_fields = ["created_at", "deleted_at", "deleted"]

        extra_kwargs = {"full": {"write_only": True}}


class DeleteActionSerializer(serializers.Serializer):
    full = serializers.BooleanField(default=False)
