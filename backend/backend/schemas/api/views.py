from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from backend.schemas.models import Schema

from backend.schemas.api.serializers import SchemaSerializer, DeleteActionSerializer


class SchemaViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        if self.action == "list":
            return Schema.revision_manager.get_schemas()
        return queryset

    def perform_update(self, serializer):
        # Get the marker from the serializer's validated data
        marker = serializer.validated_data.get("marker")
        file = serializer.validated_data.get("file")
        name = serializer.validated_data.get("name")
        description = serializer.validated_data.get("description")
        # Check for existing models with the same marker
        existing_instance = (
            Schema.objects.filter(marker=marker)
            .exclude(pk=serializer.instance.pk)
            .first()
        )

        if existing_instance:
            # Create a new model instance if an existing one with the same marker is found
            new_data = existing_instance.copy()
            new_data.file = file if file else existing_instance.file
            new_data.name = name if name else existing_instance.name
            new_data.description = (
                description if description else existing_instance.description
            )

            new_data.save()
        else:
            # Proceed with the update if no existing model with the same marker is found
            serializer.save()

    def list(self, request):
        files = self.get_queryset()
        serializer = SchemaSerializer(files, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        serializer = DeleteActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_delete = serializer.data.get("full")
        instance = self.get_object()

        instance.delete(full_delete)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def logs(self, request, pk=None):
        instance = self.get_object()
        logs = instance.get_logs()
        serializer = SchemaSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def head(self, request, pk=None):
        instance = self.get_object()
        revisions = instance.get_head()
        serializer = SchemaSerializer(revisions)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        try:
            instance = self.get_object()
            response = FileResponse(
                instance.file,
                as_attachment=True,
                filename="{0}.yaml".format(instance.name),
            )
            return response
        except FileNotFoundError:
            raise Http404("File not found")
