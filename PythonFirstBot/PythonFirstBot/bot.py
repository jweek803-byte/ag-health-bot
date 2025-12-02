import telebot
from telebot import types
import json
import logging
import time
from datetime import datetime
from threading import Thread
import os
import sys

# ==================== НАСТРОЙКИ ====================
TOKEN = "8128076604:AAGz0zjl147Ya087U5w2d9IbV-0tS08Ja08"  # ← Заменить на актуальный токен
ADMIN_ID = 1690527494  # ← Только твой Telegram ID
CHANNEL = "@AG_HealthCenter"
CHANNEL_LINK = "https://t.me/AG_HealthCenter"

# ==================== ЛОГИ ====================
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ==================== БОТ ====================
bot = telebot.TeleBot(TOKEN)

# ==================== БАЗА ПОЛЬЗОВАТЕЛЕЙ ====================
try:
    with open("users.json", "r", encoding="utf-8") as f:
        USERS = json.load(f)
except:
    USERS = {}


def save_db():
    try:
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(USERS, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения БД: {e}")


# ==================== ГЛАВНОЕ МЕНЮ ====================
def main_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add("Каталог оборудования", "Болезни и рекомендации")
    m.add("Записаться на процедуру", "Наш канал")
    return m


# ==================== КАТАЛОГ ====================
catalog = [{
    "name":
    "Массажёр для глаз",
    "photo":
    "eye.jpg",
    "desc":
    "Комплексный уход за глазами 8 в 1\n• Снимает усталость и сухость\n• Улучшает кровообращение сетчатки\n• Тепло + компрессия + вибрация\n• 15 минут в день = профилактика катаракты"
}, {
    "name":
    "Health Expert — 25 программ",
    "photo":
    "expert.jpg",
    "desc":
    "Профессиональный физиоаппарат\n• 25 программ\n• 4 аппликатора одновременно\n• Миостимуляция + лазер + магниты\n• Лечит суставы, позвоночник, сосуды"
}, {
    "name":
    "Водородная колба / генератор",
    "photo":
    "hydrogen.jpg",
    "desc":
    "Самый мощный антиоксидант\n• До 5000 ppb водорода\n• Нейтрализует свободные радикалы\n• Повышает энергию и иммунитет\n• 300 мл за 5 минут"
}, {
    "name":
    "Лазерный пояс Body Belt",
    "photo":
    "belt.jpg",
    "desc":
    "Лазерное омоложение поясницы\n• 650 нм лазер\n• Ускоряет кровоток и лимфу\n• Убирает боли и целлюлит\n• 20–30 минут в день"
}, {
    "name":
    "Турмалиновый ковёр Relax",
    "photo":
    "relax.jpg",
    "desc":
    "Глубокий прогрев + детокс\n• 62 камня турмалина и нефрита\n• ИК-тепло до 70°C\n• Отрицательные ионы\n• Размер 180×60 см"
}, {
    "name":
    "Kenta — ударно-волновой массажёр",
    "photo":
    "kenta.jpg",
    "desc":
    "Ударно-волновая терапия\n• 32 уровня\n• 60 турмалиновых камней\n• Разбивает солевые отложения\n• Эффект с первого сеанса"
}]


def catalog_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i, item in enumerate(catalog):
        kb.add(
            types.InlineKeyboardButton(item["name"],
                                       callback_data=f"item_{i}"))
    kb.add(
        types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    return kb


# ==================== БОЛЕЗНИ ====================
diseases = {
    "Артроз": {
        "desc": "Хроническое разрушение хряща",
        "symptoms": "Боль при движении, хруст",
        "consequences": "Деформация суставов",
        "equipment": "Турмалиновый ковёр + Health Expert"
    },
    "Артрит": {
        "desc": "Воспаление суставов",
        "symptoms": "Отёк покраснение",
        "consequences": "Разрушение сустава",
        "equipment": "Лазерный пояс Body Belt"
    },
    "Диабет": {
        "desc": "Нарушение обмена сахара",
        "symptoms": "Жажда слабость",
        "consequences": "Поражение сосудов",
        "equipment": "Водород + ковёр Relax"
    },
    "Катаракта": {
        "desc": "Помутнение хрусталика",
        "symptoms": "Затуманенное зрение",
        "consequences": "Слепота",
        "equipment": "Массажёр для глаз"
    },
    "Бессонница": {
        "desc": "Трудности с засыпанием",
        "symptoms": "Частые пробуждения",
        "consequences": "Стресс",
        "equipment": "Ковёр Relax перед сном"
    },
    "Головные боли": {
        "desc": "Хронические боли",
        "symptoms": "Пульсация тошнота",
        "consequences": "Снижение работоспособности",
        "equipment": "Ковёр + лазерный пояс"
    },
    "Варикоз": {
        "desc": "Расширение вен",
        "symptoms": "Тяжесть в ногах",
        "consequences": "Тромбозы",
        "equipment": "Прогревания на ковре"
    },
    "Лимфостаз": {
        "desc": "Застой лимфы",
        "symptoms": "Отёки",
        "consequences": "Инфекции",
        "equipment": "Ковёр + водород"
    },
    "Остеохондроз": {
        "desc": "Поражение позвоночника",
        "symptoms": "Боли в спине",
        "consequences": "Грыжи",
        "equipment": "Health Expert + Kenta"
    },
    "Жировой гепатоз": {
        "desc": "Жир в печени",
        "symptoms": "Тяжесть в боку",
        "consequences": "Цирроз",
        "equipment": "Ковёр Relax + водород"
    }
}


def diseases_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for d in diseases:
        kb.add(types.InlineKeyboardButton(d, callback_data=f"disease_{d}"))
    kb.add(
        types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    return kb


# ==================== ЕЖЕДНЕВНЫЕ ПОСТЫ ====================
daily_posts = [
    "День 1 | Водородная вода — главный антиоксидант XXI века\nМолекулярный водород нейтрализует только вредные радикалы, не трогая полезные. 300 мл в день = энергия, крепкий сон, иммунитет.",
    "День 2 | Турмалиновый ковёр Relax — ваш личный физиотерапевт\n62 камня при 70°C излучают ИК-тепло и отрицательные ионы. 20 минут = глубокий прогрев и детокс.",
    "День 3 | Лазерный пояс Body Belt — не только от боли\nЛазер 650 нм проникает на 5–7 см, ускоряет кровоток и выработку коллагена. Боли уходят, целлюлит уменьшается.",
    "День 4 | Ударно-волновая терапия без страха\nKenta 32 уровня — начинайте с мягких. Остеохондроз и солевые отложения уходят за 7–10 сеансов.",
    "День 5 | Защита зрения\nМассажёр для глаз: тепло, компрессия, вибрация. 15 минут в день — профилактика катаракты и глаукомы.",
    "День 6 | Health Expert — 25 программ\nЛечите колени, поясницу, шею одновременно. 4 аппликатора + лазер + магниты = домашний физиокабинет.",
    "День 7 | Результаты за месяц\n• 92 человека спят лучше\n• 68 меньше боли в спине\n• 47 прилив сил от водорода\nВы следующий?",
    "День 8 | Шея после компьютера\n15 минут на ковре Relax — напряжение, хруст и головные боли уходят.",
    "День 9 | Водород + спорт\n300 мл водородной воды после тренировки ускоряют восстановление мышц.",
    "День 10 | Почему врачи любят турмалин\nНагретый турмалин очищает организм на клеточном уровне.",
    "День 11 | Body Belt и женское здоровье\nПомогает при менструальных болях, улучшает кровообращение и уменьшает целлюлит.",
    "День 12 | Как уснуть за 10 минут\n20 минут на ковре Relax — 9 из 10 засыпают прямо на нём.",
    "День 13 | Водород против усталости\nЧерез 3–5 дней ясная голова и море энергии.",
    "День 14 | Kenta и стопы\n7 минут массажа стоп = снятие усталости всего тела и профилактика плоскостопия.",
    "День 15 | Замедление старения\nВодород — враг свободных радикалов, ускоряющих старение.",
    "День 16 | Грыжа позвоночника\nBody Belt + ковёр Relax — облегчение уже через 10 дней.",
    "День 17 | Турмалин и давление\nПрогревание помогает при ВСД и скачках давления.",
    "День 18 | Поддержка печени\nВодород + мягкие прогревания на ковре — восстановление после праздников.",
    "День 19 | Варикоз отступает\nПрограммы лимфодренажа на Health Expert уменьшают отёки.",
    "День 20 | Зрение у детей и взрослых\nМассажёр замедляет близорукость и снимает спазм аккомодации.",
    "День 21 | Почему болит спина\nМалоподвижность. Решение: ковёр Relax + Kenta каждый день.",
    "День 22 | Водород и мозг\nПроходит через гематоэнцефалический барьер и защищает мозг.",
    "День 23 | Body Belt и мужское здоровье\nУлучшение при простатите через 10–14 дней.",
    "День 24 | Снятие стресса за 15 минут\nЛягте на ковёр Relax — напряжение уходит.",
    "День 25 | Kenta вместо мануальщика\nЭкономия денег на сеансах.",
    "День 26 | Водород и кожа\nЗдоровая кожа, меньше морщин, быстрее заживление.",
    "День 27 | Турмалин и суставы\nГлубокое тепло снимает воспаление и восстанавливает хрящ.",
    "День 28 | Лазерный пояс и живот\n20 минут в день = уменьшение объёмов, лучшее пищеварение.",
    "День 29 | Главная причина старения\nСвободные радикалы. Оружие — водородная вода.",
    "День 30 | 30 дней — 30 фактов\nЗавтра новый цикл! Вы выбрали устройство для здоровья?"
]


# ==================== ЕЖЕДНЕВНАЯ РАССЫЛКА ====================
def send_daily_post():
    try:
        with open("post_index.json", "r") as f:
            idx = json.load(f).get("index", 0)
    except:
        idx = 0

    post = daily_posts[idx % 30]
    try:
        bot.send_message(CHANNEL, post, parse_mode="Markdown")
        logger.info(f"Пост {idx + 1}/30 отправлен")
    except Exception as e:
        logger.error(f"Ошибка отправки поста: {e}")

    idx = (idx + 1) % 30
    with open("post_index.json", "w") as f:
        json.dump({"index": idx}, f)


def daily_scheduler():
    while True:
        now = datetime.now()
        if now.hour == 10 and now.minute < 5:
            today = now.strftime("%Y-%m-%d")
            if not hasattr(
                    daily_scheduler,
                    "sent_today") or daily_scheduler.sent_today != today:
                send_daily_post()
                daily_scheduler.sent_today = today
        time.sleep(60)


# ==================== ОБРАБОТЧИКИ ====================
@bot.message_handler(commands=['start'])
def start(m):
    uid = str(m.from_user.id)
    if uid not in USERS:
        USERS[uid] = {"name": m.from_user.first_name}
        save_db()
    bot.send_message(
        m.chat.id,
        f"Привет, {m.from_user.first_name}!\n\nЦентр Здоровья AG — восстановление и долголетие\n\nВыберите направление:",
        reply_markup=main_menu())


@bot.message_handler(commands=['restart'])
def restart_command(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Перезапуск бота...")
        logger.info("Ручной перезапуск администратором")
        os.execv(sys.executable, ['python'] + sys.argv)  # Перезапуск скрипта
    else:
        bot.send_message(message.chat.id, "Команда недоступна.")


@bot.message_handler(func=lambda m: m.text == "Каталог оборудования")
def show_catalog(m):
    bot.send_message(m.chat.id,
                     "Выберите оборудование:",
                     reply_markup=catalog_kb())


@bot.message_handler(func=lambda m: m.text == "Болезни и рекомендации")
def show_diseases(m):
    bot.send_message(m.chat.id,
                     "Выберите заболевание:",
                     reply_markup=diseases_kb())


@bot.message_handler(func=lambda m: m.text == "Записаться на процедуру")
def booking_start(m):
    msg = bot.send_message(m.chat.id, "Как к вам обращаться?")
    bot.register_next_step_handler(msg, booking_name)


def booking_name(m):
    USERS[str(m.from_user.id)] = {"name": m.text}
    save_db()
    msg = bot.send_message(m.chat.id, "Ваш телефон (с +7 или 8):")
    bot.register_next_step_handler(msg, booking_phone)


def booking_phone(m):
    USERS[str(m.from_user.id)]["phone"] = m.text
    save_db()
    msg = bot.send_message(m.chat.id, "Желаемая дата и время:")
    bot.register_next_step_handler(msg, booking_time)


def booking_time(m):
    uid = str(m.from_user.id)
    bot.send_message(m.chat.id, "Запись принята! Скоро свяжемся с вами")
    bot.send_message(
        ADMIN_ID,
        f"НОВАЯ ЗАПИСЬ\nИмя: {USERS[uid]['name']}\nТел: {USERS[uid]['phone']}\nВремя: {m.text}"
    )


@bot.message_handler(func=lambda m: m.text == "Наш канал")
def channel(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Перейти в канал AG_HealthCenter",
                                   url=CHANNEL_LINK))
    bot.send_message(m.chat.id,
                     "Отзывы, результаты, советы — всё здесь:",
                     reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("item_"))
def show_item(c):
    i = int(c.data.split("_")[1])
    item = catalog[i]
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    try:
        with open(item["photo"], "rb") as ph:
            bot.send_photo(c.message.chat.id,
                           ph,
                           caption=f"*{item['name']}*\n\n{item['desc']}",
                           parse_mode="Markdown",
                           reply_markup=kb)
    except:
        bot.send_message(c.message.chat.id,
                         f"*{item['name']}*\n\n{item['desc']}",
                         parse_mode="Markdown",
                         reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("disease_"))
def show_disease(c):
    name = c.data[8:]
    d = diseases[name]
    text = f"*{name}*\n\nОписание: {d['desc']}\nСимптомы: {d['symptoms']}\nПоследствия: {d['consequences']}\nРекомендации: {d['equipment']}"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Назад", callback_data="back_diseases"))
    kb.add(
        types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    bot.send_message(c.message.chat.id,
                     text,
                     parse_mode="Markdown",
                     reply_markup=kb)


@bot.callback_query_handler(
    func=lambda c: c.data in ["main_menu", "back_diseases"])
def back(c):
    if c.data == "main_menu":
        bot.send_message(c.message.chat.id,
                         "Главное меню:",
                         reply_markup=main_menu())
    else:
        bot.send_message(c.message.chat.id,
                         "Выберите заболевание:",
                         reply_markup=diseases_kb())


# ==================== АВТО-РЕСТАРТ ====================
def run_bot():
    while True:
        try:
            logger.info("Запуск polling...")
            bot.infinity_polling(none_stop=True, interval=0, timeout=90)
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}. Перезапуск через 5 сек...")
            time.sleep(5)


# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    Thread(target=daily_scheduler, daemon=True).start()
    Thread(target=run_bot, daemon=True).start()
    logger.info("Бот запущен навсегда — 10:00 по Алматы ежедневные посты")
    while True:
        time.sleep(3600)
