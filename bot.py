import logging
from collections import Counter
from textblob import TextBlob
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8359437673:AAHgvqyk3-gRdfXktsOwMPanMQmMUh8Z1dc"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------- TEXT ANALYSE ----------
def analyze_text(text):
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    most_common = Counter(words).most_common(5)

    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    if sentiment > 0:
        mood = "😊 Positiv"
    elif sentiment < 0:
        mood = "😞 Negativ"
    else:
        mood = "😐 Neutral"

    result = (
        f"📊 Analyse:\n\n"
        f"Wörter: {word_count}\n"
        f"Zeichen: {char_count}\n\n"
        f"Häufigste Wörter:\n"
    )

    for word, count in most_common:
        result += f"- {word}: {count}x\n"

    result += f"\nStimmung: {mood} (Score: {round(sentiment, 2)})"

    return result


# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hallo!\n\n"
        "Sende mir einen Text mit:\n"
        "/analyse DEIN_TEXT\n\n"
        "Oder benutze /help"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Verfügbare Befehle:\n\n"
        "/start - Bot starten\n"
        "/help - Hilfe anzeigen\n"
        "/analyse TEXT - Text analysieren\n"
        "/stats - Info über Bot"
    )


async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠ Bitte gib einen Text an!\nBeispiel:\n/analyse Hallo Welt")
        return

    text = " ".join(context.args)
    result = analyze_text(text)
    await update.message.reply_text(result)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Ich analysiere Texte nach Wortanzahl, Zeichen & Stimmung.")


# ---------- MAIN ----------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyse))
    app.add_handler(CommandHandler("stats", stats))

    print("Bot läuft...")
    app.run_polling()