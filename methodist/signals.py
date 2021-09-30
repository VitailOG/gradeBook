from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def delete_incorrect_users(sender, instance, created, **kwargs):
    try:
        if instance.student.year_entry is None:
            instance.student.delete()
    except Exception:
        print('Object not exist')
        pass


