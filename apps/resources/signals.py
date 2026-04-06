import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender='resources.Resource')
def resource_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"--- SIGNAL: Yangi darslik qo'shildi: {instance.title} ---")

        author = instance.author
        if author:
            author.points += 10
            author.save()
            print(f"--- {author.username} ga 10 ball berildi! ---")


@receiver(post_delete, sender='resources.Resource')
def resource_post_delete(sender, instance, **kwargs):
    if instance.file:
        try:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
                print(f"--- {instance.title} fayli xotiradan o'chirildi ---")
        except Exception as e:
            print(f"Faylni o'chirishda xatolik: {e}")