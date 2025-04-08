from django.utils import timezone

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model class that provides 'created_at' and 'updated_at'
    fields
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    """
    Manager class for soft-deletable models that filters out
    deleted instances.Provides additional methods for querying deleted and
    non-deleted instances.
    """

    def get_queryset(self):
        """
        Returns a queryset that filters out deleted instances
        """
        return super().get_queryset().filter(deleted_at__isnull=True)

    def with_trashed(self):
        """
        Returns a queryset including all instances, including deleted ones
        """
        return super().get_queryset()

    def trashed(self):
        """
        Returns a queryset that only includes deleted instances
        """
        return super().get_queryset().filter(deleted_at__isnull=False)


class SoftDeleteWithBaseModel(BaseModel):
    """
    Abstract base model class that adds soft-delete functionality to a model.
    """

    deleted_at = models.DateTimeField(null=True)

    objects = SoftDeleteManager()

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        abstract = True

    def delete(self, *args, **kwargs):
        """
        This function sets the "deleted_at" attribute to the current datetime
        and saves the object.
        """
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        This function reStore a deleted object by setting its "deleted_at"
        attribute to None and saving it.
        """
        self.deleted_at = None
        self.save()

    @classmethod
    def bulk_delete(cls, filters):
        """
        Performs a bulk delete operation on objects matching the
        specified filters
        """
        cls.objects.filter(**filters).update(deleted_at=timezone.now())
