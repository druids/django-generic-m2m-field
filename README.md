Prolog
======

`Django-generic-m2m-field` extends the Django framework with a `GenericManyToManyField`. The field is similar to the standard `ManyToManyField` but uses Django's `GenericForeignKey` to relate to many different models.

Installation
------------

- Install `django-generic-m2m-field` with the `pip` command:

```bash
pip install django-generic-m2m-field
```

- Add `'generic_m2m_field'` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Django apps...
    'generic_m2m_field',
]
```

Usage
-----
Imagine having an e-mail message log model where you need to relate more of different kinds of objects to the message:

```python
from django.db import models
from generic_m2m_field.models import GenericManyToManyField


class EmailMessage(models.Model):

    recipient = models.EmailField(verbose_name=_('recipient'), blank=False, null=False)
    sender = models.EmailField(verbose_name=_('sender'), blank=False, null=False)
    subject = models.TextField(verbose_name=_('subject'), blank=False, null=False)
    related_objects = GenericManyToManyField()

```

Now you can join your `EmailMessage` instance with any instance of any other model (User in this example):


```python
from django.contrib.auth.models import User

user1, user2 = User.objects.all()

email_message = EmailMessage.objects.first()

# Add user1 and user2
email_message.related_objects.add(user1)
email_message.related_objects.add(user1, user2)

# Remove user2
email_message.related_objects.remove(user2)

# Clear all relations
email_message.related_objects.clear()

# Set relations
email_message.related_objects.set(user2)

# Get all related object pks of User model (casted to right type)
email_message.related_objects.get_object_pks(User)

# Get all related object pks of User model
email_message.related_objects.get_objects(User)

```

Multiple DB
-----------

Django doesn't support foreign key for multiple databases. If you want to use generic m2m relation for models stored in different databases you can use ``MultipleDBGenericManyToManyField`` with the same way as GenericManyToManyField


```python
from django.db import models
from generic_m2m_field.models import MultipleDBGenericManyToManyField


class EmailMessage(models.Model):

    recipient = models.EmailField(verbose_name=_('recipient'), blank=False, null=False)
    sender = models.EmailField(verbose_name=_('sender'), blank=False, null=False)
    subject = models.TextField(verbose_name=_('subject'), blank=False, null=False)
    related_objects = MultipleDBGenericManyToManyField()

```

Named generic m2m field DB
--------------------------

Sometimes you want to name your relations. You can use ``NamedGenericManyToManyField`` for this purpose.

```python
from django.db import models
from generic_m2m_field.models import NamedGenericManyToManyField


class EmailMessage(models.Model):

    recipient = models.EmailField(verbose_name=_('recipient'), blank=False, null=False)
    sender = models.EmailField(verbose_name=_('sender'), blank=False, null=False)
    subject = models.TextField(verbose_name=_('subject'), blank=False, null=False)
    related_objects = NamedGenericManyToManyField()

```

Now you can set relations with names:


```python
from django.contrib.auth.models import User

user1, user2 = User.objects.all()

email_message = EmailMessage.objects.first()

# Add user1 and user2
email_message.related_objects.add(author=user1)
email_message.related_objects.add(watcher=user2)

# Read author and watcher
email_message.related_objects.author  # return user1
email_message.related_objects.watcher  # return user2
email_message.related_objects.to_attr_dict()  # return AttrDict(author=user1, watcher=user2) 

# Remove watcher
email_message.related_objects.remove(['watcher'])

# Clear all relations
email_message.related_objects.clear()

# Set relations
email_message.related_objects.set(author=user2)
```
