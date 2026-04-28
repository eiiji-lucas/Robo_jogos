import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from sports_data import get_todays_games


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("THE_SPORTS_DB_API_KEY", "1")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Olá! Sou seu robô de jogos. Use /jogos ou /hoje para receber a lista dos jogos do dia em futebol, basquete e Valorant."
    )


async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not TELEGRAM_TOKEN:
        await update.message.reply_text(
            "Token do Telegram não configurado. Verifique o arquivo .env e atualize TELEGRAM_TOKEN."
        )
        return

    games = get_todays_games(API_KEY)
    if not games:
        await update.message.reply_text(
            "Não foi possível buscar os jogos do dia no momento. Tente novamente mais tarde."
        )
        return

    message = "📅 <b>Jogos do dia:</b>\n\n"
    for i, game in enumerate(games, 1):
        message += (
            f"{i}. <b>{game['sport']}</b> - {game['league']}\n"
            f"   🕐 {game['time']} | {game['home']} x {game['away']}\n"
            f"   📺 {game['broadcast']}\n\n"
        )
    
    await update.message.reply_text(message, parse_mode="HTML")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Comandos disponíveis:\n/jogos ou /hoje - Mostra a agenda de jogos do dia."
    )


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN não encontrado. Crie um arquivo .env com a chave do bot.")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jogos", jogos))
    app.add_handler(CommandHandler("hoje", jogos))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("Bot iniciado. Aguardando comandos...")
    app.run_polling()


if __name__ == "__main__":
    main()
