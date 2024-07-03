from rest_framework.serializers import ValidationError
from django.utils.deconstruct import deconstructible
from backend.schemas.schema import Schema
from pydantic import ValidationError as PydanticValidationError
import yaml


@deconstructible
class FileValidator(object):
    requires_context = True
    error_messages = {
        "content_type": "Files of type %(content_type)s are not supported.",
    }
    extensions = ["yml", "yaml"]

    def __call__(self, file, serializer_field):
        content = file.read()
        try:
            yaml_content = yaml.safe_load(content)
            Schema(**yaml_content)
        except yaml.YAMLError as e:
            raise ValidationError(f"Invalid YAML content: {str(e)}")
        except PydanticValidationError as e:
            raise ValidationError(f"Invalid schema content: {str(e)}")
        finally:
            file.seek(0)
