import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

GROUP_A_ID = -1003904086062
TOPIC_A_ID = 305

GROUP_B_ID = -1002415746359
TOPIC_B_ID = 3302852

ARABIC_PLACE = (GROUP_A_ID, TOPIC_A_ID)
ITALIAN_PLACE = (GROUP_B_ID, TOPIC_B_ID)

ALLOWED_PLACES = {
    ARABIC_PLACE,
    ITALIAN_PLACE,
}

is_busy = False


async def send_countdown(context: ContextTypes.DEFAULT_TYPE, chat_id: int, topic_id: int, title_text: str):
    sent_messages = []

    title_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=title_text,
        message_thread_id=topic_id
    )
    sent_messages.append(title_msg)

    msg3 = await context.bot.send_message(
        chat_id=chat_id,
        text="3",
        message_thread_id=topic_id
    )
    sent_messages.append(msg3)
    await asyncio.sleep(1)

    msg2 = await context.bot.send_message(
        chat_id=chat_id,
        text="2",
        message_thread_id=topic_id
    )
    sent_messages.append(msg2)
    await asyncio.sleep(1)

    msg1 = await context.bot.send_message(
        chat_id=chat_id,
        text="1",
        message_thread_id=topic_id
    )
    sent_messages.append(msg1)
    await asyncio.sleep(1)

    msg_go = await context.bot.send_message(
        chat_id=chat_id,
        text="Go",
        message_thread_id=topic_id
    )
    sent_messages.append(msg_go)

    await asyncio.sleep(1)

    for msg in sent_messages:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        except Exception:
            pass


async def s_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_busy

    message = update.effective_message
    source_chat_id = update.effective_chat.id
    source_topic_id = message.message_thread_id
    source_place = (source_chat_id, source_topic_id)

    if source_place not in ALLOWED_PLACES:
        return

    if is_busy:
        return

    is_busy = True

    try:
        if source_place == ARABIC_PLACE:
            title_a = "Count"
            title_b = "Arabic Group Searching - Conto"
        else:
            title_a = "Italian Group Searching - Count"
            title_b = "Conto"

        await asyncio.gather(
            send_countdown(context, GROUP_A_ID, TOPIC_A_ID, title_a),
            send_countdown(context, GROUP_B_ID, TOPIC_B_ID, title_b)
        )

        await asyncio.sleep(10)

    finally:
        is_busy = False


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("s", s_command))
    app.run_polling()


if __name__ == "__main__":
    main()
