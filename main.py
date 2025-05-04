import os

from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, \
    ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, Application

from api import getNews, getGames, getLastGames, getStats

URL = "https://qjn4yrtgsgmgwtbktqsnsx5t.agents.do-ai.run/api/v1/chat/completions"

async def comandos_app(app : Application):
    comandos = [
        BotCommand("start", "Inicia o bot"),
        BotCommand("noticias", "Mostra as ultimas noticias"),
        BotCommand("partidas", "Mostra as últimas partidas"),
        BotCommand("stats", "Pergunte as estatisticas da FURIA!"),
        BotCommand("proximos_jogos", "Mostra as proximas partidas da Pantera"),
    ]

    await app.bot.set_my_commands(comandos)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("Ver Partidas Recentes", callback_data="Partidas Recentes"),
        ],
        [
            InlineKeyboardButton("Ver Noticias Furiosas", callback_data="Noticias Furiosas"),
        ],
        [
            InlineKeyboardButton("Ver Proximas Partidas", callback_data="Proximas Partidas"),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=(
            "🤖 *BEM VINDO AO BOT FURIOSO DA FURIA!* 🤖\n\n"
            "AQUI É O SEU LUGAR PARA FICAR POR DENTRO DE TUDO QUE ACONTECE NA FURIA!\n\n"
            "*AQUI VOCÊ VAI ENCONTRAR:*\n"
            "🎮 JOGOS\n"
            "📊 RESULTADOS\n"
            "📈 ESTATÍSTICAS\n"
            "📰 NOTÍCIAS\n"
            "E MUITO MAIS!\n"
        ),
        parse_mode="Markdown",
        reply_markup=markup
    )

    await update.message.reply_text(
        text=(
            "Utilize \"/stats\" para descobrir as estatisticas da FURIA CS!\n\n"
            "Exemplo : /stats Quais as estatisticas do Fallen?\n"
        ),
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    stat = getStats(text)

    await update.message.reply_text(text=stat)


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):

    news = getNews()

    if len(news) != 0:

        news_string = "📰 *NOTÍCIAS DA FURIA:* 📰\n\n"
        for i in range(0, 3):
            artigo = news[i]
            news_string += f"• {artigo['title']} - {artigo['link']}\n"

        await update.effective_chat.send_message(text=news_string, parse_mode="Markdown")


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games = getGames()

    if games:
        mensagem = "📅 Próximos Jogos da FURIA\n\n"
        mensagem += (f"📌 {games.get("evento")}\n🆚 "
                     f"{games.get("times")[0]} x {games.get("times")[1]}\n📆 "
                     f"{games.get("data")}\n⏰ "
                     f"{games.get("hora")}\n\n")

        await update.effective_chat.send_message(text=mensagem, parse_mode="Markdown")
    else:
        await update.effective_chat.send_message(text="Nenhum jogo encontrado para a pantera.")

async def ultimos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lastGames = getLastGames()

    mensagem = "📅 Partidas Recentes da FURIA\n\n"
    status = "✅"
    for game in lastGames:

        if game.get("resultado").endswith("0") or game.get("resultado").endswith("1"):
            status = "❌"
        mensagem += (f"📌 {game.get("evento")}\n🆚 "
                    f"{game.get("adversario")}\n📆 "
                    f"{game.get("data")}\n📊 "
                    f"Resultado: {game.get("resultado")} {status}\n\n")

    await update.effective_chat.send_message(text=mensagem, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "Partidas Recentes":
        await ultimos_jogos(update, context)
    elif query.data == "Noticias Furiosas":
        await noticias(update, context)

    elif query.data == "Proximas Partidas":
        await proximos_jogos(update, context)


def start_bot():
    load_dotenv()
    token = os.getenv("TOKEN")

    app = ApplicationBuilder().token(token).post_init(comandos_app).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('stats', stats))
    app.add_handler(CommandHandler('noticias', noticias))
    app.add_handler(CommandHandler('partidas', ultimos_jogos))
    app.add_handler(CommandHandler('proximos_jogos', proximos_jogos))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()



if __name__ == '__main__':

    print("Bot Iniciado com sucesso!")
    start_bot()

