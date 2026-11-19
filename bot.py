import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = """Добро пожаловать в KUMSIYAT 🇨🇳

Китай — это огромные возможности, если знать, как с ним работать.
Я более 5 лет занимаюсь практическими закупками в Китае, изучаю рынок, работаю с поставщиками и делюсь опытом, который помогает другим уверенно начать свой путь.

Здесь ты научишься самостоятельно выкупать товары, находить поставщиков и разбираться в денежных переводах и обмене валют.

KUMSIYAT — твой проводник в мир закупок из Китая.
Выбирай направление и начинай!"""

PRODUCTS = {
    "course": {
        "title": "Самовыкуп из Китая",
        "price": "9 990 ₽",
        "description": (
            "Научись самостоятельно покупать товары из Китая, работать с китайскими "
            "площадками, находить надёжных поставщиков и рассчитывать стоимость заказа."
        ),
        "content": (
            "В обучении:\n\n"
            "1. Alipay — регистрация и верификация, пароли, пополнение и переводы, "
            "привязка к китайским площадкам, работа с обменником.\n\n"
            "2. 1688 и Taobao — регистрация, интерфейс, поиск товаров, избранное и корзина, "
            "оплата, отслеживание, возвраты и обмены, общение с продавцами, проверка "
            "поставщиков и фабрик, отзывы и рейтинги, размерные ряды, расчёт себестоимости "
            "и наценки, закупки с нуля и 1688 Plus.\n\n"
            "3. Poizon, WeChat, 95 и Pinduoduo — регистрация, интерфейс, добавление "
            "поставщиков в WeChat и оформление заказов.\n\n"
            "4. Карго — адрес склада, что такое карго, страховка, система получения "
            "посылки и расчёт веса."
        ),
    },
    "suppliers": {
        "title": "База поставщиков из Китая",
        "price": "7 900 ₽",
        "description": (
            "Хочешь работать напрямую с поставщиками из Китая? В этом разделе ты получишь "
            "доступ к отдельному продукту KUMSIYAT — базе поставщиков из Китая. "
            "База создана для тех, кто хочет находить товары и поставщиков для своих "
            "закупок и бизнеса."
        ),
        "content": "Доступ к отдельному продукту KUMSIYAT — базе поставщиков из Китая.",
    },
    "currency": {
        "title": "Обучение обмену валют",
        "price": "15 900 ₽",
        "description": (
            "Обучение по обмену валют: методика, инструкции, видео и все необходимые материалы."
        ),
        "content": "Внутри — методика, видеоуроки, инструкции и все учебные материалы.",
    },
    "bundle": {
        "title": "Самовыкуп + база поставщиков",
        "price": "14 900 ₽",
        "description": (
            "Комплект для тех, кто хочет научиться самостоятельно выкупать товары из Китая "
            "и получить доступ к базе поставщиков."
        ),
        "content": (
            "В комплект входят:\n"
            "• Обучение «Самовыкуп из Китая» — 9 990 ₽\n"
            "• База поставщиков из Китая — 7 900 ₽\n\n"
            "Отдельно: 17 890 ₽.\n"
            "В комплекте: 14 900 ₽.\n"
            "Экономия: 2 990 ₽."
        ),
    },
}

MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("Самовыкуп из Китая", callback_data="course")],
    [InlineKeyboardButton("База поставщиков", callback_data="suppliers")],
    [InlineKeyboardButton("Обучение обмену валют", callback_data="currency")],
    [InlineKeyboardButton("Самовыкуп + база поставщиков", callback_data="bundle")],
    [InlineKeyboardButton("Об авторе", callback_data="about")],
])

def product_keyboard(key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Купить обучение", callback_data=f"buy:{key}")],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="home")],
    ])

async def show_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(WELCOME_TEXT, reply_markup=MAIN_MENU)
    elif update.callback_query:
        await update.callback_query.edit_message_text(WELCOME_TEXT, reply_markup=MAIN_MENU)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_home(update, context)

async def show_product(update: Update, key: str) -> None:
    product = PRODUCTS[key]
    text = (
        f"🇨🇳 {product['title']}\n\n"
        f"{product['description']}\n\n"
        f"{product['content']}\n\n"
        f"Стоимость: {product['price']}"
    )
    query = update.callback_query
    await query.edit_message_text(text, reply_markup=product_keyboard(key))

async def show_about(update: Update) -> None:
    text = (
        "❤️ Об авторе KUMSIYAT\n\n"
        "Я более 5 лет занимаюсь практическими закупками в Китае, изучаю рынок "
        "и работаю с поставщиками.\n\n"
        "В KUMSIYAT я делюсь опытом и знаниями, которые помогают увереннее "
        "начать свой путь в закупках из Китая."
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="home")]
    ])
    await update.callback_query.edit_message_text(text, reply_markup=keyboard)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE, key: str) -> None:
    product = PRODUCTS[key]
    text = (
        f"🇨🇳 {product['title']}\n\n"
        f"{product['description']}\n\n"
        f"{product['content']}\n\n"
        f"Стоимость: {product['price']}"
    )
    await update.message.reply_text(text, reply_markup=product_keyboard(key))

async def course_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await menu_command(update, context, "course")

async def suppliers_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await menu_command(update, context, "suppliers")

async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await menu_command(update, context, "currency")

async def bundle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await menu_command(update, context, "bundle")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data or ""

    if data.startswith("buy:"):
        await query.answer(
            "Покупка скоро будет доступна. Сейчас оформление оплаты ещё не подключено.",
            show_alert=True,
        )
    else:
        await query.answer()
        if data == "home":
            await show_home(update, context)
        elif data == "about":
            await show_about(update)
        elif data in PRODUCTS:
            await show_product(update, data)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Ошибка при обработке обновления", exc_info=context.error)

def main() -> None:
    bot_token = os.environ.get("BOT_TOKEN", "").strip()
    base_url = os.environ.get("WEBHOOK_URL", "").strip().rstrip("/")
    webhook_secret = os.environ.get("WEBHOOK_SECRET", "").strip()
    port = int(os.environ.get("PORT", "10000"))

    if not bot_token:
        raise RuntimeError("Не задана переменная окружения BOT_TOKEN.")
    if not base_url.startswith("https://"):
        raise RuntimeError("WEBHOOK_URL должен быть полным адресом Render, начиная с https://")
    if not webhook_secret or len(webhook_secret) < 16:
        raise RuntimeError("Задай WEBHOOK_SECRET длиной не менее 16 символов.")

    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("course", course_command))
    application.add_handler(CommandHandler("suppliers", suppliers_command))
    application.add_handler(CommandHandler("currency", currency_command))
    application.add_handler(CommandHandler("bundle", bundle_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    # Telegram sends updates to this HTTPS URL. Render terminates HTTPS
    # and forwards requests to this app on the internal PORT.
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=webhook_secret,
        webhook_url=f"{base_url}/{webhook_secret}",
        secret_token=webhook_secret,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=False,
        bootstrap_retries=-1,
    )

if __name__ == "__main__":
    main()
