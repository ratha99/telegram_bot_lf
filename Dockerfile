# Use official Python image as base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (not required for Telegram bot, but useful for debugging)
EXPOSE 8080

# Run the bot
CMD ["python", "telegram_bot.py"]
