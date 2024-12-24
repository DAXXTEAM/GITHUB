# GitHub Manager Telegram Bot

A Telegram bot to manage GitHub repositories using Python and Pyrogram.

## Features
- Create GitHub repositories
- Upload files from zip archives
- Automatic file extraction and upload

## Setup

1. Get your Telegram API credentials:
   - Go to https://my.telegram.org/apps
   - Create a new application
   - Copy API_ID and API_HASH

2. Create a Telegram bot:
   - Talk to @BotFather on Telegram
   - Create new bot with /newbot
   - Copy the bot token

3. Get GitHub token:
   - Go to GitHub Settings
   - Developer settings > Personal access tokens
   - Generate new token with 'repo' scope

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit .env and add your tokens:
   ```
   API_ID=your_telegram_api_id
   API_HASH=your_telegram_api_hash
   BOT_TOKEN=your_telegram_bot_token
   GITHUB_TOKEN=your_github_token
   ```

6. Run the bot:
   ```bash
   python bot.py
   ```

## Commands
- /start - Show welcome message and commands
- /create_repo [name] [description] - Create new repository
- /upload_zip - Reply to a zip file to upload its contents