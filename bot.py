from pyrogram import Client, filters
from config import Config
from bot_commands import Commands

# Initialize bot
bot = Client(
    "github_manager_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Register command handlers
@bot.on_message(filters.command("start"))
async def start(client, message):
    await Commands.start_command(client, message)

@bot.on_message(filters.command("help"))
async def help(client, message):
    await Commands.help_command(client, message)

@bot.on_message(filters.command("login"))
async def login(client, message):
    await Commands.login_command(client, message)

@bot.on_message(filters.command("logout"))
async def logout(client, message):
    await Commands.logout_command(client, message)

@bot.on_message(filters.command("create_repo"))
async def create_repo(client, message):
    await Commands.create_repo(client, message)

@bot.on_message(filters.command("list_repos"))
async def list_repos(client, message):
    await Commands.list_repos(client, message)

@bot.on_message(filters.command("upload_zip"))
async def upload_zip(client, message):
    await Commands.upload_zip(client, message)

@bot.on_message(filters.command("search_repos"))
async def search_repos(client, message):
    await Commands.search_repos(client, message)

@bot.on_message(filters.command("create_issue"))
async def create_issue(client, message):
    await Commands.create_issue(client, message)

@bot.on_message(filters.command("list_issues"))
async def list_issues(client, message):
    await Commands.list_issues(client, message)

@bot.on_message(filters.command("fork_repo"))
async def fork_repo(client, message):
    await Commands.fork_repo(client, message)

def main():
    print("Starting bot...")
    bot.run()

if __name__ == "__main__":
    main()