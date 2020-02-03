from django.db import models

from generic_m2m_field.models import GenericManyToManyField


class GenericManyToManyModel(models.Model):

    related_objects = GenericManyToManyField()


class OneRelatedObject(models.Model):
    pass


class SecondRelatedObject(models.Model):

    id = models.CharField(primary_key=True, max_length=10)
