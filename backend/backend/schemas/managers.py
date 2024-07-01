from django.db.models import OuterRef, Subquery
from django.db.models import Manager


class RevisionManager(Manager):
    def get_schemas(self):

        latest_entry_subquery = (
            self.filter(marker=OuterRef("marker"))
            .order_by("-created_at")
            .values("pk")[:1]
        )

        latest_unique_rows = self.filter(pk__in=Subquery(latest_entry_subquery))
        return latest_unique_rows
