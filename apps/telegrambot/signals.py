import os
import requests
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.resources.models import Resource

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8564194100:AAFqXH5w_nkm3iATK8XU6U24PI2CHg5qib4")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@Rahmatillqodirov")
SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:8000")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def send_telegram_message(message):
    """Kanalga xabar yuborish."""
    url = f"{BASE_URL}sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.ok:
            print(f"--- KANAL: xabar yuborildi ---")
        else:
            print(f"--- KANAL xato: {response.status_code} ---")
    except Exception as e:
        print(f"Telegram ulanish xatosi: {e}")


@receiver(post_save, sender=Resource)
def resource_post_save(sender, instance, created, **kwargs):
    """Yangi resurs qo'shilganda kanalga xabar yuborish."""
    if created:
        sinf = f"{instance.class_level}-sinf" if instance.class_level else ""
        verified = " (Tasdiqlangan)" if instance.is_verified else " (Tekshirilmoqda)"
        author = instance.author.get_full_name() or instance.author.username
        text = (
            f"Yangi darslik qo'shildi!\n\n"
            f"<b>{instance.title}</b>\n"
            f"Fan: {instance.subject.name} {sinf}\n"
            f"Muallif: {author}{verified}\n\n"
            f"Ko'rish: {SITE_URL}/resources/{instance.id}/"
        )
        send_telegram_message(text)


@receiver(post_delete, sender=Resource)
def resource_post_delete(sender, instance, **kwargs):
    """Resurs o'chirilganda faylni ham o'chirish."""
    if instance.file:
        try:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
                print(f"--- {instance.title} fayli o'chirildi ---")
        except Exception as e:
            print(f"Faylni o'chirishda xato: {e}")
