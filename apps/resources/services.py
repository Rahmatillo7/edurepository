import os

def increment_download_count(resource):
    resource.download_count += 1
    resource.save(update_fields=['download_count'])

def delete_old_file(instance):
    if instance.pk:
        try:
            old_file = instance.__class__.objects.get(pk=instance.pk).file
            if old_file and old_file != instance.file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        except instance.DoesNotExist:
            pass
