from attrdict import AttrDict

from django.core.exceptions import MultipleObjectsReturned

from germanium.test_cases.default import GermaniumTestCase
from germanium.tools import assert_equal, assert_is_none, assert_raises

from apps.app.models import (
    GenericManyToManyModel, MultipleDBGenericManyToManyModel, OneRelatedObject, SecondRelatedObject,
    NamedGenericManyToManyModel
)


class GenericManyToManyTestCase(GermaniumTestCase):

    def test_generic_m2m_should_add_related_object(self):
        m2m_inst = GenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        assert_equal(m2m_inst.related_objects.count(), 0)
        m2m_inst.related_objects.add(related_object_inst1)
        assert_equal(m2m_inst.related_objects.count(), 1)

        m2m_inst.related_objects.add(related_object_inst2, related_object_inst3)

        assert_equal(m2m_inst.related_objects.count(), 3)

        # Duplicate objects are not added
        m2m_inst.related_objects.add(related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 3)

    def test_generic_m2m_should_clear_related_object(self):
        m2m_inst = GenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 2)

        m2m_inst.related_objects.clear()
        assert_equal(m2m_inst.related_objects.count(), 0)

    def test_generic_m2m_should_set_related_object(self):
        m2m_inst = GenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 2)

        m2m_inst.related_objects.set(related_object_inst3)
        assert_equal(m2m_inst.related_objects.count(), 1)
        assert_equal(m2m_inst.related_objects.get().object_id, str(related_object_inst3.pk))

    def test_generic_m2m_should_remove_related_object(self):
        m2m_inst = GenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2, related_object_inst3)
        assert_equal(m2m_inst.related_objects.count(), 3)

        m2m_inst.related_objects.remove(related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 2)
        assert_equal(
            set(m2m_inst.related_objects.values_list('object_id', flat=True)),
            {str(related_object_inst1.pk), str(related_object_inst3.pk)}
        )

    def test_generic_m2m_manager_should_return_object_pks_according_to_model_class(self):
        m2m_inst = GenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2, related_object_inst3)

        assert_equal(list(m2m_inst.related_objects.get_object_pks(SecondRelatedObject)), [related_object_inst2.pk])
        assert_equal(
            list(m2m_inst.related_objects.get_object_pks(OneRelatedObject)),
            [related_object_inst1.pk, related_object_inst3.pk]
        )

    def test_generic_m2m_manager_should_return_object_according_to_model_class(self):
        m2m_inst = GenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2, related_object_inst3)

        assert_equal(list(m2m_inst.related_objects.get_objects(SecondRelatedObject)), [related_object_inst2])
        assert_equal(
            list(m2m_inst.related_objects.get_objects(OneRelatedObject)),
            [related_object_inst1, related_object_inst3]
        )

    def test_multiple_db_generic_m2m_should_add_related_object(self):
        m2m_inst = MultipleDBGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        assert_equal(m2m_inst.related_objects.count(), 0)
        m2m_inst.related_objects.add(related_object_inst1)
        assert_equal(m2m_inst.related_objects.count(), 1)

        m2m_inst.related_objects.add(related_object_inst2, related_object_inst3)

        assert_equal(m2m_inst.related_objects.count(), 3)

        # Duplicate objects are not added
        m2m_inst.related_objects.add(related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 3)

    def test_multiple_db_generic_m2m_should_clear_related_object(self):
        m2m_inst = MultipleDBGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 2)

        m2m_inst.related_objects.clear()
        assert_equal(m2m_inst.related_objects.count(), 0)

    def test_multiple_db_generic_m2m_should_set_related_object(self):
        m2m_inst = MultipleDBGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 2)

        m2m_inst.related_objects.set(related_object_inst3)
        assert_equal(m2m_inst.related_objects.count(), 1)
        assert_equal(m2m_inst.related_objects.get().object_id, str(related_object_inst3.pk))

    def test_multiple_db_generic_m2m_should_remove_related_object(self):
        m2m_inst = MultipleDBGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2, related_object_inst3)
        assert_equal(m2m_inst.related_objects.count(), 3)

        m2m_inst.related_objects.remove(related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 2)
        assert_equal(
            set(m2m_inst.related_objects.values_list('object_id', flat=True)),
            {str(related_object_inst1.pk), str(related_object_inst3.pk)}
        )

    def test_multiple_db_generic_m2m_manager_should_return_object_pks_according_to_model_class(self):
        m2m_inst = MultipleDBGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2, related_object_inst3)

        assert_equal(list(m2m_inst.related_objects.get_object_pks(SecondRelatedObject)), [related_object_inst2.pk])
        assert_equal(
            list(m2m_inst.related_objects.get_object_pks(OneRelatedObject)),
            [related_object_inst1.pk, related_object_inst3.pk]
        )

    def test_generic_m2m_manager_should_return_object_according_to_model_class(self):
        m2m_inst = MultipleDBGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2, related_object_inst3)

        assert_equal(list(m2m_inst.related_objects.get_objects(SecondRelatedObject)), [related_object_inst2])
        assert_equal(
            list(m2m_inst.related_objects.get_objects(OneRelatedObject)),
            [related_object_inst1, related_object_inst3]
        )

    def test_generic_m2m_manager_should_get_object_or_none_accroding_to_model_class(self):
        m2m_inst = MultipleDBGenericManyToManyModel.objects.create()

        assert_is_none(m2m_inst.related_objects.get_object_or_none(OneRelatedObject))

        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(related_object_inst1, related_object_inst2, related_object_inst3)

        assert_equal(m2m_inst.related_objects.get_object_or_none(SecondRelatedObject), related_object_inst2)

        with assert_raises(MultipleObjectsReturned):
            m2m_inst.related_objects.get_object_or_none(OneRelatedObject)

        assert_equal(
            m2m_inst.related_objects.get_object_or_none(OneRelatedObject, related_object_inst3.pk), related_object_inst3
        )

    def test_named_generic_m2m_should_add_related_object(self):
        m2m_inst = NamedGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        assert_equal(m2m_inst.related_objects.count(), 0)
        m2m_inst.related_objects.add(related_object1=related_object_inst1)
        assert_equal(m2m_inst.related_objects.count(), 1)
        assert_equal(m2m_inst.related_objects.related_object1, related_object_inst1)

        m2m_inst.related_objects.add(related_object2=related_object_inst2, related_object3=related_object_inst3)
        assert_equal(m2m_inst.related_objects.count(), 3)
        assert_equal(m2m_inst.related_objects.related_object1, related_object_inst1)
        assert_equal(m2m_inst.related_objects.related_object2, related_object_inst2)
        assert_equal(m2m_inst.related_objects.related_object3, related_object_inst3)

        # Duplicate named objects are updated
        m2m_inst.related_objects.add(related_object1=related_object_inst2)
        assert_equal(m2m_inst.related_objects.count(), 3)
        assert_equal(m2m_inst.related_objects.related_object1, related_object_inst2)
        assert_equal(m2m_inst.related_objects.related_object2, related_object_inst2)
        assert_equal(m2m_inst.related_objects.related_object3, related_object_inst3)

    def test_named_generic_m2m_should_clear_related_object(self):
        m2m_inst = NamedGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')

        m2m_inst.related_objects.add(
            related_inst1=related_object_inst1, related_inst2=related_object_inst2
        )
        assert_equal(m2m_inst.related_objects.count(), 2)

        m2m_inst.related_objects.clear()
        assert_equal(m2m_inst.related_objects.count(), 0)

    def test_named_generic_m2m_should_set_related_object(self):
        m2m_inst = NamedGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(
            related_inst1=related_object_inst1,
            related_inst2=related_object_inst2
        )
        assert_equal(m2m_inst.related_objects.count(), 2)

        m2m_inst.related_objects.set(
            related_inst3=related_object_inst3
        )
        assert_equal(m2m_inst.related_objects.count(), 1)
        assert_equal(m2m_inst.related_objects.related_inst3, related_object_inst3)
        assert_equal(m2m_inst.related_objects.get().object_id, str(related_object_inst3.pk))

    def test_named_generic_m2m_should_remove_related_object(self):
        m2m_inst = NamedGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')
        related_object_inst3 = OneRelatedObject.objects.create()

        m2m_inst.related_objects.add(
            related_object1=related_object_inst1,
            related_object2=related_object_inst2,
            related_object3=related_object_inst3
        )
        assert_equal(m2m_inst.related_objects.count(), 3)

        m2m_inst.related_objects.remove('related_object2')
        assert_equal(m2m_inst.related_objects.count(), 2)
        assert_equal(
            set(m2m_inst.related_objects.values_list('object_id', flat=True)),
            {str(related_object_inst1.pk), str(related_object_inst3.pk)}
        )

    def test_named_generic_m2m_should_return_related_object_by_name_or_attribut_error(self):
        m2m_inst = NamedGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')

        m2m_inst.related_objects.add(
            related_object1=related_object_inst1,
            related_object2=related_object_inst2
        )
        assert_equal(m2m_inst.related_objects.related_object1, related_object_inst1)
        assert_equal(m2m_inst.related_objects.related_object2, related_object_inst2)
        with assert_raises(AttributeError):
            m2m_inst.related_object3

    def test_named_generic_m2m_should_return_attr_dict_of_related_objects(self):
        m2m_inst = NamedGenericManyToManyModel.objects.create()
        related_object_inst1 = OneRelatedObject.objects.create()
        related_object_inst2 = SecondRelatedObject.objects.create(id='unique')

        m2m_inst.related_objects.add(
            related_object1=related_object_inst1,
            related_object2=related_object_inst2
        )
        assert_equal(m2m_inst.related_objects.to_attr_dict(), AttrDict(
            related_object1=related_object_inst1,
            related_object2=related_object_inst2
        ))
