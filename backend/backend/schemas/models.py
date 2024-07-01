# encoding: utf-8

import uuid
import difflib
from datetime import date, datetime
from typing import ClassVar
from django.db import models
from django.core.validators import FileExtensionValidator
from backend.schemas.managers import RevisionManager


class Schema(models.Model):
    marker = models.CharField(max_length=36, editable=False, null=True, db_index=True)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField()
    file = models.FileField(
        upload_to="schemas/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(allowed_extensions=["yml", "yaml"])],
    )
    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    revision_manager = RevisionManager()

    def delete(self, full=False, *args, **kwargs):
        if full:
            super(models.Model, self).delete(args, kwargs)
        else:
            self.deleted = True
            self.deleted_at = datetime.now()

            self.save()

    def delete_all(self, full=False, *args, **kwargs):
        for obj in self.get_logs():
            obj.delete(full, *args, **kwargs)

    def copy(self):
        duplicate = self.__class__()
        for field in self._meta.fields:
            pk = field.primary_key
            auto_field = getattr(field, "auto_now_add", False)

            if not (pk or auto_field):
                value = getattr(self, field.name)
                setattr(duplicate, field.name, value)

        duplicate.save()

        return duplicate

    objects: ClassVar[models.Manager] = models.Manager()

    def get_logs(self):
        qs = self.__class__.objects.filter(marker=self.marker).order_by("-created_at")

        return qs

    def is_head(self):
        return self.id >= max([version.id for version in self.get_logs()])

    def revert_to(self, date: date):
        revert_to_obj = (
            self.get_logs()
            .objects.filter(**{"created_at__lte": date})
            .order("-created_at")[0]
        )

        if revert_to_obj:
            raise IndexError("Cannot find a matching revision near that date.")
        else:
            return revert_to_obj.revert()

    def get_head(self):
        return self.get_logs()[0]

    def make_head(self):
        if not self.is_head():
            self.save()

    def show_diff(self, to, field):
        frm = (getattr(self, field)).split()
        to = (getattr(to, field)).split()
        differ = difflib.HtmlDiff()
        return differ.make_table(frm, to)

    def revert(self):
        self.validate_unique()
        return self.copy()

    def save(self, *args, **kwargs):
        if not self.marker:
            self.marker = uuid.uuid4().hex

        self.validate_unique()
        super(self).save(*args, **kwargs)
