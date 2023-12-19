import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'settings')
import django
django.setup()

from django.contrib.auth.models import Group, Permission, ContentType


mod = Group(name='moderator')
mod.save()

rep = Group(name='representative')
rep.save()

content = ContentType.objects.get(app_label='auth', model='user')

mod_perm = Permission(codename='moderator', content_type_id=content.id, name='custom')
mod_perm.save()

rep_perm = Permission(codename='representative', content_type_id=content.id, name='custom')
rep_perm.save()

mod.permissions.add(mod_perm)
rep.permissions.add(rep_perm)
