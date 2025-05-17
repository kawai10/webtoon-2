from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_date__isnull=True)


class TimeStampModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True)

    objects = SoftDeleteManager()
    objects_all = models.Manager()

    class Meta:
        abstract = True
        ordering = ["created_date"]

    def delete(self, using=None, keep_parents=False, hard_delete=False):
        if hard_delete:
            return super().delete(using=using, keep_parents=keep_parents)
        self.deleted_date = timezone.now()
        self.save(update_fields=['deleted_date'])

    def restore(self):
        self.deleted_date = None
        self.save(update_fields=['deleted_date'])