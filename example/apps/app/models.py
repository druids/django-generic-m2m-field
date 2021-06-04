from django.db import models

from generic_m2m_field.models import (
    GenericManyToManyField, MultipleDBGenericManyToManyField, NamedGenericManyToManyField
)


class GenericManyToManyModel(models.Model):

    related_objects = GenericManyToManyField()


class MultipleDBGenericManyToManyModel(models.Model):

    related_objects = MultipleDBGenericManyToManyField()


class NamedGenericManyToManyModel(models.Model):

    related_objects = NamedGenericManyToManyField()


class OneRelatedObject(models.Model):
    pass


class SecondRelatedObject(models.Model):

    id = models.CharField(primary_key=True, max_length=10)
