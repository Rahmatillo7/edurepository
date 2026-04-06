from django.apps import AppConfig

class TelegrambotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.telegrambot'

    def ready(self):
        # Bu yerda faqat signallarni import qilamiz
        import apps.telegrambot.signals
