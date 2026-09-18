import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# ---------- Logging ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- Config ----------
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN env variable is missing!")

# ---------- Text tools ----------
def reverse_text(t: str) -> str:
    return t[::-1]

def upper_text(t: str) -> str:
    return t.upper()

def lower_text(t: str) -> str:
    return t.lower()

def title_text(t: str) -> str:
    return t.title()

def word_count(t: str):
    words = t.split()
    chars = len(t)
    chars_no_space = len(t.replace(" ", ""))
    return len(words), chars, chars_no_space

def remove_extra_spaces(t: str) -> str:
    return " ".join(t.split())

def base64_encode(t: str) -> str:
    import base64
    return base64.b64encode(t.encode()).decode()

def base64_decode(t: str) -> str:
    import base64
    try:
        return base64.b64decode(t.encode()).decode()
    except Exception:
        return "❌ Invalid Base64 input."


# ---------- Command handlers ----------
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Welcome to TextExxp Bot!*\n\n"
        "I'm a fast, free text utility bot. Send me any text and I'll help you:\n\n"
        "• 🔄 Reverse it\n"
        "• 🔠 Convert to UPPER / lower / Title Case\n"
        "• 📊 Count words & characters\n"
        "• 🧹 Clean extra spaces\n"
        "• 🔐 Encode / Decode Base64\n\n"
        "Use /help to see all commands.\n\n"
        "⚡ No ads. No spam. Just text tools."
    )
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data="help"),
         InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 *TextExxp Bot – Commands*\n\n"
        "*Basic commands*\n"
        "• /start – Welcome screen\n"
        "• /help – Show this help\n"
        "• /about – About this bot\n\n"
        "*Text tools* (send text after the command)\n"
        "• `/reverse your text` – Reverse text\n"
        "• `/upper your text` – UPPERCASE\n"
        "• `/lower your text` – lowercase\n"
        "• `/title your text` – Title Case\n"
        "• `/count your text` – Words & character count\n"
        "• `/clean your text` – Remove extra spaces\n"
        "• `/b64e your text` – Encode to Base64\n"
        "• `/b64d your text` – Decode from Base64\n\n"
        "💡 *Tip:* You can also just send any plain message and I'll ask what to do with it."
    )
    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def about_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ *About TextExxp Bot*\n\n"
        "TextExxp is a lightweight, privacy-friendly text utility bot.\n\n"
        "• 🚫 No ads\n"
        "• 🚫 No data storage\n"
        "• 🚫 No spam\n"
        "• ✅ Free forever\n"
        "• ✅ Works 24/7 on Railway\n\n"
        "Made with ❤️ using python-telegram-bot."
    )
    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ---------- Generic text-tool commands ----------
def extract_arg(update: Update):
    parts = update.message.text.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else ""


async def reverse_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/reverse your text`", parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text(reverse_text(arg))

async def upper_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/upper your text`", parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text(upper_text(arg))

async def lower_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/lower your text`", parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text(lower_text(arg))

async def title_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/title your text`", parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text(title_text(arg))

async def count_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/count your text`", parse_mode=ParseMode.MARKDOWN)
    w, c, cns = word_count(arg)
    await update.message.reply_text(
        f"📊 *Text stats*\n\n• Words: `{w}`\n• Characters: `{c}`\n• Characters (no spaces): `{cns}`",
        parse_mode=ParseMode.MARKDOWN,
    )

async def clean_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/clean your text`", parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text(remove_extra_spaces(arg))

async def b64e_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/b64e your text`", parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text(base64_encode(arg))

async def b64d_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    arg = extract_arg(update)
    if not arg:
        return await update.message.reply_text("Usage: `/b64d your text`", parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text(base64_decode(arg))


# ---------- Plain text handler ----------
async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["last_text"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("🔄 Reverse", callback_data="reverse"),
         InlineKeyboardButton("🔠 UPPER", callback_data="upper")],
        [InlineKeyboardButton("🔡 lower", callback_data="lower"),
         InlineKeyboardButton("🔤 Title", callback_data="title")],
        [InlineKeyboardButton("📊 Count", callback_data="count"),
         InlineKeyboardButton("🧹 Clean", callback_data="clean")],
        [InlineKeyboardButton("🔐 Base64 Encode", callback_data="b64e")],
    ]
    await update.message.reply_text(
        "✅ Got your text. What should I do with it?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ---------- Button callbacks ----------
async def button_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "help":
        return await help_cmd(update, ctx)
    if data == "about":
        return await about_cmd(update, ctx)

    text = ctx.user_data.get("last_text", "")
    if not text:
        return await q.message.reply_text("⚠️ Please send some text first.")

    if data == "reverse":
        result = reverse_text(text)
    elif data == "upper":
        result = upper_text(text)
    elif data == "lower":
        result = lower_text(text)
    elif data == "title":
        result = title_text(text)
    elif data == "count":
        w, c, cns = word_count(text)
        result = f"📊 Words: {w}\nCharacters: {c}\nNo spaces: {cns}"
    elif data == "clean":
        result = remove_extra_spaces(text)
    elif data == "b64e":
        result = base64_encode(text)
    else:
        result = "❓ Unknown action."

    await q.message.reply_text(f"```\n{result}\n```", parse_mode=ParseMode.MARKDOWN)


# ---------- Entry ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("reverse", reverse_cmd))
    app.add_handler(CommandHandler("upper", upper_cmd))
    app.add_handler(CommandHandler("lower", lower_cmd))
    app.add_handler(CommandHandler("title", title_cmd))
    app.add_handler(CommandHandler("count", count_cmd))
    app.add_handler(CommandHandler("clean", clean_cmd))
    app.add_handler(CommandHandler("b64e", b64e_cmd))
    app.add_handler(CommandHandler("b64d", b64d_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("🚀 TextExxp Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
