# -*- coding: utf-8 -*-
"""
Edu Repository - Telegram Bot
Loyiha strukturasiga to'liq mos, xatosiz bot.
"""
import os
import sys
import time
import requests
import django

def find_project_root():
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5):
        if os.path.exists(os.path.join(current, "manage.py")):
            return current
        current = os.path.dirname(current)
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "manage.py")):
        return cwd
    raise RuntimeError("manage.py topilmadi!")

PROJECT_ROOT = find_project_root()
print(f"PROJECT_ROOT: {PROJECT_ROOT}")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("Django muvaffaqiyatli ulandi!")
except Exception as e:
    print(f"Django ulanishida xato: {e}")
    sys.exit(1)

from apps.resources.models import Resource, Category, Subject
from apps.users.models import User
from apps.interactions.models import Comment, Favorite

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8564194100:AAFqXH5w_nkm3iATK8XU6U24PI2CHg5qib4")
CHANNEL_ID = os.environ.get("@qodirovcodes", "@Rahmatillqodirov")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:8000")

user_state = {}



def api_call(method, payload):
    try:
        url = f"{BASE_URL}{method}"
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Timeout: {method}")
    except requests.exceptions.ConnectionError:
        print("Internet uzildi...")
    except Exception as e:
        print(f"API xato ({method}): {e}")
    return {}


def send_message(chat_id, text, reply_markup=None, parse_mode="HTML"):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api_call("sendMessage", payload)


def send_message_to_channel(text):
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    result = api_call("sendMessage", payload)
    if result.get("ok"):
        print(f"Kanalga yuborildi: {CHANNEL_ID}")
    else:
        print(f"Kanal xato: {result.get('description', 'Noma`lum')}")


def answer_callback_query(callback_query_id, text=""):
    api_call("answerCallbackQuery", {"callback_query_id": callback_query_id, "text": text})


def main_menu_keyboard():
    return {
        "keyboard": [
            [{"text": "Resurslar"}, {"text": "Qidirish"}],
            [{"text": "Kategoriyalar"}, {"text": "Sevimlilar"}],
            [{"text": "Statistika"}, {"text": "Yordam"}],
        ],
        "resize_keyboard": True,
        "persistent": True,
    }


def inline_subjects_keyboard(category_id=None):
    try:
        if category_id:
            subjects = Subject.objects.filter(category_id=category_id)
        else:
            subjects = Subject.objects.all()
        buttons = []
        row = []
        for i, subj in enumerate(subjects):
            row.append({"text": subj.name, "callback_data": f"subject_{subj.id}"})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([{"text": "Bosh menyu", "callback_data": "main_menu"}])
        return {"inline_keyboard": buttons}
    except Exception as e:
        print(f"Fanlar klaviaturasi xato: {e}")
        return {"inline_keyboard": [[{"text": "Xato", "callback_data": "main_menu"}]]}


def inline_categories_keyboard():
    try:
        categories = Category.objects.all()
        buttons = []
        for cat in categories:
            buttons.append([{"text": cat.name, "callback_data": f"category_{cat.id}"}])
        buttons.append([{"text": "Bosh menyu", "callback_data": "main_menu"}])
        return {"inline_keyboard": buttons}
    except Exception as e:
        print(f"Kategoriyalar klaviaturasi xato: {e}")
        return {"inline_keyboard": [[{"text": "Xato", "callback_data": "main_menu"}]]}


def inline_class_keyboard(subject_id):
    buttons = []
    row = []
    for i in range(1, 12):
        row.append({"text": f"{i}-sinf", "callback_data": f"class_{subject_id}_{i}"})
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([{"text": "Orqaga", "callback_data": f"subject_{subject_id}"}])
    return {"inline_keyboard": buttons}


def inline_resources_keyboard(resources, subject_id, class_level, page=0, per_page=5):
    start = page * per_page
    end = start + per_page
    chunk = resources[start:end]
    total = len(resources)
    buttons = []
    for res in chunk:
        buttons.append([{"text": res.title[:45], "callback_data": f"resource_{res.id}"}])
    nav = []
    if page > 0:
        nav.append({"text": "Oldingi", "callback_data": f"page_{subject_id}_{class_level}_{page - 1}"})
    if end < total:
        nav.append({"text": "Keyingi", "callback_data": f"page_{subject_id}_{class_level}_{page + 1}"})
    if nav:
        buttons.append(nav)
    buttons.append([{"text": f"{start + 1}-{min(end, total)}/{total} ta", "callback_data": "noop"}])
    buttons.append([{"text": "Orqaga", "callback_data": f"subject_{subject_id}"}])
    return {"inline_keyboard": buttons}


def inline_resource_detail_keyboard(resource):
    buttons = [
        [{"text": "Yuklab olish", "url": f"{SITE_URL}/resources/{resource.id}/download/"}],
        [{"text": "Saytda korish", "url": f"{SITE_URL}/resources/{resource.id}/"}],
        [{"text": "Orqaga", "callback_data": "back_to_list"}],
    ]
    return {"inline_keyboard": buttons}



def format_resource(resource):
    lang_map = {"uz": "O'zbek", "ru": "Rus", "en": "Ingliz"}
    lang = lang_map.get(resource.language, resource.language)
    sinf = f"{resource.class_level}-sinf" if resource.class_level else "Belgilanmagan"
    verified = "Tasdiqlangan" if resource.is_verified else "Tekshirilmoqda"
    author_name = resource.author.get_full_name() or resource.author.username
    desc = resource.description[:200] + ('...' if len(resource.description) > 200 else '')
    return (
        f"<b>{resource.title}</b>\n\n"
        f"Fan: <b>{resource.subject.name}</b>\n"
        f"Sinf: <b>{sinf}</b>\n"
        f"Til: <b>{lang}</b>\n"
        f"Muallif: <b>{author_name}</b>\n"
        f"Tavsif: {desc}\n"
        f"Ko'rishlar: <b>{resource.view_count}</b> | Yuklamalar: <b>{resource.download_count}</b>\n"
        f"Holat: {verified}"
    )


def format_statistics():
    try:
        total_resources = Resource.objects.filter(is_verified=True).count()
        total_users = User.objects.count()
        total_categories = Category.objects.count()
        total_subjects = Subject.objects.count()
        total_downloads = sum(Resource.objects.values_list('download_count', flat=True))
        total_views = sum(Resource.objects.values_list('view_count', flat=True))
        return (
            f"<b>Sayt statistikasi</b>\n\n"
            f"Resurslar: <b>{total_resources}</b> ta\n"
            f"Foydalanuvchilar: <b>{total_users}</b> ta\n"
            f"Kategoriyalar: <b>{total_categories}</b> ta\n"
            f"Fanlar: <b>{total_subjects}</b> ta\n"
            f"Jami yuklamalar: <b>{total_downloads}</b>\n"
            f"Jami ko'rishlar: <b>{total_views}</b>"
        )
    except Exception as e:
        return f"Statistika olishda xato: {e}"



def handle_start(chat_id, user_data):
    first_name = user_data.get("first_name", "Foydalanuvchi")
    text = (
        f"Salom, <b>{first_name}</b>!\n\n"
        f"<b>Edu Repository</b> botiga xush kelibsiz!\n\n"
        f"Bu bot orqali darsliklar va o'quv materiallarga "
        f"qulay kirishingiz mumkin.\n\n"
        f"Sayt: <a href='{SITE_URL}'>{SITE_URL}</a>"
    )
    send_message(chat_id, text, reply_markup=main_menu_keyboard())


def handle_help(chat_id):
    text = (
        f"<b>Bot imkoniyatlari:</b>\n\n"
        f"Resurslar — So'nggi qo'shilgan materiallar\n"
        f"Qidirish — Nom bo'yicha qidirish\n"
        f"Kategoriyalar — Turkum bo'yicha ko'rish\n"
        f"Sevimlilar — Saqlangan resurslar\n"
        f"Statistika — Umumiy ma'lumotlar\n\n"
        f"Sayt: <a href='{SITE_URL}'>{SITE_URL}</a>"
    )
    send_message(chat_id, text)


def handle_resources_list(chat_id):
    try:
        resources = Resource.objects.filter(is_verified=True).order_by('-created_at')[:10]
        if not resources:
            send_message(chat_id, "Hozircha tasdiqlangan resurslar yo'q.")
            return
        text = f"<b>So'nggi resurslar</b> ({resources.count()} ta):"
        buttons = []
        for res in resources:
            buttons.append([{"text": res.title[:45], "callback_data": f"resource_{res.id}"}])
        buttons.append([{"text": "Kategoriya bo'yicha", "callback_data": "show_categories"}])
        send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})
    except Exception as e:
        send_message(chat_id, f"Xato yuz berdi: {e}")


def handle_categories(chat_id):
    try:
        count = Category.objects.count()
        if count == 0:
            send_message(chat_id, "Hozircha kategoriyalar yo'q.")
            return
        text = f"<b>Kategoriyalar</b> ({count} ta):"
        send_message(chat_id, text, reply_markup=inline_categories_keyboard())
    except Exception as e:
        send_message(chat_id, f"Xato: {e}")


def handle_search_prompt(chat_id):
    user_state[chat_id] = {"step": "waiting_search"}
    send_message(
        chat_id,
        "Resurs nomi yoki kalit so'z kiriting:\n(Bekor qilish: /cancel)",
        reply_markup={"remove_keyboard": True}
    )


def handle_search_query(chat_id, query):
    try:
        results = (
            Resource.objects.filter(is_verified=True, title__icontains=query) |
            Resource.objects.filter(is_verified=True, description__icontains=query)
        ).distinct()[:10]

        if not results:
            send_message(
                chat_id,
                f"'<b>{query}</b>' bo'yicha hech narsa topilmadi.",
                reply_markup=main_menu_keyboard()
            )
            user_state.pop(chat_id, None)
            return

        text = f"'<b>{query}</b>' — <b>{results.count()}</b> ta natija:"
        buttons = []
        for res in results:
            buttons.append([{"text": res.title[:45], "callback_data": f"resource_{res.id}"}])
        buttons.append([{"text": "Bosh menyu", "callback_data": "main_menu"}])
        send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})
        user_state.pop(chat_id, None)
    except Exception as e:
        send_message(chat_id, f"Qidirishda xato: {e}")
        user_state.pop(chat_id, None)


def handle_statistics(chat_id):
    send_message(chat_id, format_statistics())


def handle_resource_detail(chat_id, resource_id):
    try:
        resource = Resource.objects.select_related('author', 'subject').get(id=resource_id)
        send_message(chat_id, format_resource(resource), reply_markup=inline_resource_detail_keyboard(resource))
    except Resource.DoesNotExist:
        send_message(chat_id, "Resurs topilmadi yoki o'chirilgan.")
    except Exception as e:
        send_message(chat_id, f"Xato: {e}")


def handle_subject_resources(chat_id, subject_id, class_level=None, page=0):
    try:
        subject = Subject.objects.get(id=subject_id)
        if class_level is None:
            text = f"<b>{subject.name}</b>\n\nQaysi sinfni tanlaysiz?"
            send_message(chat_id, text, reply_markup=inline_class_keyboard(subject_id))
            return

        resources = list(
            Resource.objects.filter(
                is_verified=True, subject_id=subject_id, class_level=class_level
            ).order_by('-created_at')
        )
        if not resources:
            send_message(
                chat_id,
                f"<b>{subject.name}</b> ({class_level}-sinf) uchun resurslar yo'q.",
                reply_markup={"inline_keyboard": [[{"text": "Orqaga", "callback_data": f"subject_{subject_id}"}]]}
            )
            return

        text = f"<b>{subject.name} — {class_level}-sinf</b>\n{len(resources)} ta resurs:"
        send_message(
            chat_id, text,
            reply_markup=inline_resources_keyboard(resources, subject_id, class_level, page)
        )
    except Subject.DoesNotExist:
        send_message(chat_id, "Fan topilmadi.")
    except Exception as e:
        send_message(chat_id, f"Xato: {e}")


def handle_favorites(chat_id, telegram_id):
    try:
        user = User.objects.filter(telegram_id=str(telegram_id)).first()
        if not user:
            send_message(
                chat_id,
                f"Sevimlilaringizni ko'rish uchun saytda profilingizga "
                f"Telegram ID ({telegram_id}) ni kiriting.\n\n"
                f"Sayt: <a href='{SITE_URL}'>{SITE_URL}</a>"
            )
            return

        favorites = Favorite.objects.filter(user=user).select_related('resource')[:20]
        if not favorites:
            send_message(chat_id, "Hozircha sevimli resurslaringiz yo'q.")
            return

        text = f"<b>Sevimlilaringiz</b> ({favorites.count()} ta):"
        buttons = []
        for fav in favorites:
            buttons.append([{"text": fav.resource.title[:45], "callback_data": f"resource_{fav.resource.id}"}])
        buttons.append([{"text": "Bosh menyu", "callback_data": "main_menu"}])
        send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})
    except Exception as e:
        send_message(chat_id, f"Xato: {e}")



def handle_callback(callback):
    query_id = callback["id"]
    chat_id = callback["message"]["chat"]["id"]
    data = callback.get("data", "")
    user_data = callback.get("from", {})

    answer_callback_query(query_id)

    if data == "main_menu":
        handle_start(chat_id, user_data)
    elif data == "show_categories":
        handle_categories(chat_id)
    elif data.startswith("category_"):
        cat_id = int(data.split("_")[1])
        send_message(chat_id, "Fanlardan birini tanlang:", reply_markup=inline_subjects_keyboard(cat_id))
    elif data.startswith("subject_"):
        subject_id = int(data.split("_")[1])
        handle_subject_resources(chat_id, subject_id)
    elif data.startswith("class_"):
        parts = data.split("_")
        subject_id = int(parts[1])
        class_level = int(parts[2])
        handle_subject_resources(chat_id, subject_id, class_level, page=0)
    elif data.startswith("page_"):
        parts = data.split("_")
        subject_id = int(parts[1])
        class_level = int(parts[2])
        page = int(parts[3])
        handle_subject_resources(chat_id, subject_id, class_level, page)
    elif data.startswith("resource_"):
        resource_id = int(data.split("_")[1])
        handle_resource_detail(chat_id, resource_id)
    elif data == "back_to_list":
        handle_resources_list(chat_id)
    elif data == "noop":
        pass



def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()
    user_data = message.get("from", {})
    telegram_id = user_data.get("id")

    # Qidiruv rejimi
    state = user_state.get(chat_id, {})
    if state.get("step") == "waiting_search" and not text.startswith("/"):
        handle_search_query(chat_id, text)
        return

    if text == "/start":
        handle_start(chat_id, user_data)
    elif text == "/help":
        handle_help(chat_id)
    elif text == "/stats":
        handle_statistics(chat_id)
    elif text == "/cancel":
        user_state.pop(chat_id, None)
        send_message(chat_id, "Bekor qilindi.", reply_markup=main_menu_keyboard())

    elif text == "Resurslar":
        handle_resources_list(chat_id)
    elif text == "Qidirish":
        handle_search_prompt(chat_id)
    elif text == "Kategoriyalar":
        handle_categories(chat_id)
    elif text == "Sevimlilar":
        handle_favorites(chat_id, telegram_id)
    elif text == "Statistika":
        handle_statistics(chat_id)
    elif text == "Yordam":
        handle_help(chat_id)
    else:
        send_message(chat_id, "Noma'lum buyruq. Menyu tugmalaridan foydalaning.", reply_markup=main_menu_keyboard())


def handle_updates():
    last_update_id = 0
    print("--- BOT ISHGA TUSHDI ---")
    print(f"Token: ...{BOT_TOKEN[-10:]}")
    print(f"Kanal: {CHANNEL_ID}")

    while True:
        try:
            response = requests.get(
                f"{BASE_URL}getUpdates",
                params={"offset": last_update_id + 1, "timeout": 30},
                timeout=40,
            )

            if response.status_code != 200:
                print(f"Telegram xato: {response.status_code}")
                time.sleep(5)
                continue

            data = response.json()

            for update in data.get("result", []):
                last_update_id = update["update_id"]
                try:
                    if "message" in update:
                        handle_message(update["message"])
                    elif "callback_query" in update:
                        handle_callback(update["callback_query"])
                except Exception as e:
                    print(f"Update qayta ishlashda xato: {e}")

        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            print("Internet uzildi, 5 soniyada qayta urinadi...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nBot to'xtatildi.")
            break
        except Exception as e:
            print(f"Kutilmagan xato: {e}")
            time.sleep(3)


if __name__ == "__main__":
    handle_updates()