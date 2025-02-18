import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("API_URL")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create an inline keyboard with buttons
    keyboard = [
        [
            InlineKeyboardButton("Get Report Post", callback_data="get_report_post"),
            InlineKeyboardButton("Get Report User", callback_data="get_report_user"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the inline keyboard
    await update.message.reply_text("Hello! Click the button below to get the latest report.", reply_markup=reply_markup)

# Callback handler for the inline buttons
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    if query.data == "get_report_post":
        # Fetch data from the API for posts
        try:
            response = requests.get(API_URL+"/report")
            if response.status_code == 200:
                data = response.json()
                # Format the response to send to the user
                message = "📊 **Post Report**\n\n"
                for item in data:
                    if "type" in item:
                        message += "**By Type:**\n"
                        for key, value in item["type"].items():
                            message += f"- {key}: {value}\n"
                    elif "category" in item:
                        message += "\n**By Category:**\n"
                        for key, value in item["category"].items():
                            message += f"- {key}: {value}\n"
                    elif "status" in item:
                        message += "\n**By Status:**\n"
                        for key, value in item["status"].items():
                            message += f"- {key}: {value}\n"
                    elif "totalPosts" in item:
                        message += f"\n**Total Posts:** {item['totalPosts']}\n"
                await query.edit_message_text(text=message, parse_mode="Markdown")
            else:
                await query.edit_message_text(text="Failed to fetch report. Please try again later.")
        except Exception as e:
            logging.error(f"Error fetching report: {e}")
            await query.edit_message_text(text="An error occurred while fetching the report.")

    elif query.data == "get_report_user":
        # Fetch data from the API for users (you can customize this part)
        await query.edit_message_text(text="User report functionality is not implemented yet.")

# Main function to start the bot
def main():
    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Add callback handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()