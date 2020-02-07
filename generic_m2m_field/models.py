import re

from types import MethodType

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.functions import Cast
from django.utils.translation import ugettext_lazy as _

from chamber.models import SmartModel, SmartQuerySet


def camel_to_snake(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def add_objs(self, *objects):
    for obj in objects:
        self.get_or_create(
            object_ct=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )


def clear_objs(self):
    self.all().delete()


def set_objs(self, *objects):
    self.clear()
    for obj in objects:
        self.create(
            object_ct=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )


def remove_objs(self, *objects):
    for obj in objects:
        self.filter(
            object_ct=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        ).delete()


class RelatedObjectQuerySet(SmartQuerySet):

    def annotate_object_pks(self, model_class):
        pk_field = model_class._meta.pk
        if isinstance(pk_field, models.AutoField):
            pk_field = models.IntegerField()
        return self.filter(
            object_ct=ContentType.objects.get_for_model(model_class)
        ).annotate(
            object_pk=Cast('object_id', output_field=pk_field)
        )

    def get_objects(self, model_class):
        return model_class.objects.filter(pk__in=self.annotate_object_pks(model_class).values('object_pk'))

    def get_object_pks(self, model_class):
        return self.annotate_object_pks(model_class).values_list('object_pk', flat=True)

    def _filter_or_exclude(self, negate, *args, **kwargs):
        if 'object' in kwargs:
            object = kwargs.pop('object')
            kwargs.update(dict(
                object_id=object.pk,
                object_ct=ContentType.objects.get_for_model(object),
            ))
        return super()._filter_or_exclude(negate, *args, **kwargs)


class GenericManyToManyManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._is_related_manger():
            self.add = MethodType(add_objs, self)
            self.set = MethodType(set_objs, self)
            self.clear = MethodType(clear_objs, self)
            self.remove = MethodType(remove_objs, self)

    def _is_related_manger(self):
        return self.__class__.__module__ == 'django.db.models.fields.related_descriptors'


class GenericManyToMany(SmartModel):

    object_ct = models.ForeignKey(
        verbose_name=_('content type of the related object'),
        to=ContentType,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    object_id = models.TextField(
        verbose_name=_('ID of the related object'),
        null=False,
        blank=False,
        db_index=True
    )
    object = GenericForeignKey(
        'object_ct',
        'object_id'
    )
    object.verbose_name = _('related object')

    objects = GenericManyToManyManager.from_queryset(RelatedObjectQuerySet)()

    class Meta:
        abstract = True
        ordering = ('-created_at',)


def create_generic_many_to_many_intermediary_model(field, klass):
    from_name = camel_to_snake(klass.__name__).lower()

    name = '{}GenericManyToManyRelation'.format(klass._meta.object_name)
    meta = type('Meta', (), {
        'app_label': klass._meta.app_label,
        'db_tablespace': klass._meta.db_tablespace,
        'unique_together': (from_name, 'object_ct', 'object_id'),
        'apps': field.model._meta.apps,
    })
    return type(name, (GenericManyToMany,), {
        'Meta': meta,
        '__module__': klass.__module__,
        from_name: models.ForeignKey(
            klass,
            on_delete=models.CASCADE,
            related_name='_{}'.format(field.name),
            related_query_name=field.name
        ),
    })


class GenericManyToManyFieldDescriptor:

    def __init__(self, field):
        self.field = field
        self.through = field.through

    def __set__(self, instance, value):
        raise TypeError(
            'Direct assignment to the %s is prohibited. Use %s.set() instead.'
            % self._get_set_deprecation_msg_params(),
        )

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        return getattr(instance, '_{}'.format(self.field.name))


class GenericManyToManyField:

    def __init__(self, through=None):
        self.through = through

    def contribute_to_class(self, cls, name, **kwargs):
        self.model = cls
        self.name = name
        self.through = self.through or create_generic_many_to_many_intermediary_model(self, cls)
        setattr(cls, name, GenericManyToManyFieldDescriptor(self))
