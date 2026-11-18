import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Set BOT_TOKEN as an environment variable. Do not put your token in this file.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME = (
    "Добро пожаловать в KUMSIYAT 🇨🇳\n\n"
    "Китай — это огромные возможности, если знать, как с ним работать.\n\n"
    "Я более 5 лет занимаюсь практическими закупками в Китае, изучаю рынок, "
    "работаю с поставщиками и делюсь опытом, который помогает другим уверенно "
    "начать свой путь.\n\n"
    "Здесь ты научишься самостоятельно выкупать товары, находить поставщиков "
    "и разбираться в денежных переводах и обмене валют.\n\n"
    "KUMSIYAT — твой проводник в мир закупок из Китая.\n\n"
    "Выбирай направление и начинай!"
)

PRODUCTS = {
    "course": {
        "title": "🇨🇳 Самовыкуп из Китая",
        "price": "9 990 ₽",
        "text": (
            "Научись самостоятельно покупать товары из Китая, работать с китайскими "
            "площадками, находить надёжных поставщиков и рассчитывать стоимость заказа.\n\n"
            "Что входит в обучение?\n\n"
            "1. Alipay\n"
            "• Регистрация и подтверждение аккаунта\n"
            "• Пополнение и переводы\n"
            "• Привязка к китайским площадкам\n"
            "• Работа с обменниками\n\n"
            "2. 1688 и Taobao\n"
            "• Регистрация и знакомство с площадками\n"
            "• Поиск товаров и поставщиков\n"
            "• Оформление и оплата заказов\n"
            "• Общение с продавцами\n"
            "• Проверка отзывов и качества товаров\n"
            "• Расчёт стоимости заказа и наценки\n"
            "• Возвраты и отслеживание посылок\n"
            "• 1688 Plus\n\n"
            "3. Poizon, WeChat, 95 и Pinduoduo\n"
            "• Регистрация и работа с площадками\n"
            "• Поиск поставщиков\n"
            "• Общение и оформление заказов\n\n"
            "4. Карго и доставка\n"
            "• Добавление адреса склада\n"
            "• Как работает карго\n"
            "• Страхование груза\n"
            "• Получение посылки и расчёт веса\n\n"
            "Стоимость обучения: 9 990 ₽"
        ),
    },
    "suppliers": {
        "title": "📦 База поставщиков из Китая",
        "price": "7 900 ₽",
        "text": (
            "Хочешь работать напрямую с поставщиками из Китая?\n\n"
            "В этом разделе ты получишь доступ к отдельному продукту KUMSIYAT — "
            "базе поставщиков из Китая.\n\n"
            "База создана для тех, кто хочет находить товары и поставщиков "
            "для своих закупок и бизнеса.\n\n"
            "Стоимость: 7 900 ₽"
        ),
    },
    "currency": {
        "title": "💱 Обучение обмену валют",
        "price": "15 900 ₽",
        "text": (
            "Научись разбираться в обмене валют и денежных переводах, необходимых "
            "для работы с Китаем.\n\n"
            "Что входит в обучение?\n"
            "• Авторская методика\n"
            "• Подробная методичка\n"
            "• Обучающие видео\n"
            "• Все материалы, предусмотренные методикой\n\n"
            "Ты получишь материалы, которые помогут разобраться в процессе обмена "
            "валют и применять знания на практике.\n\n"
            "Стоимость обучения: 15 900 ₽"
        ),
    },
    "bundle": {
        "title": "🎁 Самовыкуп + база поставщиков",
        "price": "14 900 ₽",
        "text": (
            "Хочешь получить сразу два полезных продукта для самостоятельных "
            "закупок из Китая?\n\n"
            "В комплект входят:\n\n"
            "1. Самовыкуп из Китая\n"
            "Полное обучение самостоятельной работе с китайскими площадками, "
            "поиску товаров, оформлению заказов и доставке.\n\n"
            "2. База поставщиков\n"
            "Отдельный доступ к базе поставщиков из Китая.\n\n"
            "При отдельной покупке: 17 890 ₽\n"
            "Стоимость комплекта: 14 900 ₽\n"
            "Экономия: 2 990 ₽"
        ),
    },
}

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍️ Самовыкуп из Китая", callback_data="course")],
        [InlineKeyboardButton("📦 База поставщиков", callback_data="suppliers")],
        [InlineKeyboardButton("💱 Обучение обмену валют", callback_data="currency")],
        [InlineKeyboardButton("🎁 Самовыкуп + база поставщиков", callback_data="bundle")],
        [InlineKeyboardButton("🌸 Об авторе", callback_data="author")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Главное меню", callback_data="home")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, reply_markup=main_keyboard())

async def show_section(query, section):
    if section == "home":
        await query.edit_message_text(WELCOME, reply_markup=main_keyboard())
        return
    if section == "author":
        text = (
            "🌸 Об авторе KUMSIYAT\n\n"
            "Я более 5 лет занимаюсь практическими закупками в Китае, "
            "лично изучаю рынок и работаю с поставщиками.\n\n"
            "В KUMSIYAT я делюсь своим опытом и знаниями, чтобы помочь тебе "
            "уверенно разобраться в закупках из Китая."
        )
        await query.edit_message_text(text, reply_markup=back_keyboard())
        return
    product = PRODUCTS.get(section)
    if not product:
        await query.answer("Раздел пока недоступен.", show_alert=True)
        return
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Купить обучение", callback_data=f"buy_{section}")],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="home")],
    ])
    await query.edit_message_text(
        f"{product['title']}\n\n{product['text']}",
        reply_markup=keyboard,
    )

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ""
    if data.startswith("buy_"):
        # Payment flow intentionally disabled until payment provider and legal setup are agreed.
        await query.answer(
            "Покупка скоро будет доступна. Напишите администратору KUMSIYAT.",
            show_alert=True,
        )
        return
    await show_section(query, data)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("course", lambda u, c: start(u, c)))
    app.add_handler(CommandHandler("suppliers", lambda u, c: start(u, c)))
    app.add_handler(CommandHandler("currency", lambda u, c: start(u, c)))
    app.add_handler(CommandHandler("bundle", lambda u, c: start(u, c)))
    app.add_handler(CallbackQueryHandler(callbacks))
    logger.info("KUMSIYAT bot is starting")
    app.run_polling()

if __name__ == "__main__":
    main()
