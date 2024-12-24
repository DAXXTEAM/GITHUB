from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
from github_manager import GitHubManager
from auth_manager import AuthManager
from config import Config

auth_manager = AuthManager()

class Commands:
    @staticmethod
    async def start_command(client: Client, message: Message):
        await message.reply_text(
            "👋 Welcome to GitHub Manager Bot!\n\n"
            "🔑 First, login with your GitHub token using:\n"
            "/login [your_github_token]\n\n"
            "Available Commands:\n"
            "/help - Show all commands\n"
            "/login [token] - Login with GitHub token\n"
            "/logout - Remove your GitHub token\n"
            "/create_repo [name] [description] - Create new repository\n"
            "/list_repos - List your repositories\n"
            "/upload_zip - Reply to a zip file to upload its contents\n"
            "/delete_repo [name] - Delete a repository\n"
            "/fork_repo [owner/repo] - Fork a repository\n"
            "/search_repos [query] - Search GitHub repositories\n"
            "/create_issue [repo] [title] [body] - Create an issue\n"
            "/list_issues [repo] - List repository issues"
        )

    @staticmethod
    async def help_command(client: Client, message: Message):
        await message.reply_text(
            "📚 Available Commands:\n\n"
            "Authentication:\n"
            "/login [token] - Login with GitHub token\n"
            "/logout - Remove saved token\n\n"
            "Repository Management:\n"
            "/create_repo [name] [desc] - Create repository\n"
            "/delete_repo [name] - Delete repository\n"
            "/list_repos - Show your repositories\n"
            "/fork_repo [owner/repo] - Fork repository\n\n"
            "File Management:\n"
            "/upload_zip - Upload files from zip\n\n"
            "Issues & Search:\n"
            "/search_repos [query] - Search repositories\n"
            "/create_issue [repo] [title] [body] - Create issue\n"
            "/list_issues [repo] - List repository issues"
        )

    @staticmethod
    async def login_command(client: Client, message: Message):
        try:
            token = message.text.split(maxsplit=1)[1]
            # Verify token by creating a temporary GitHub manager
            github = GitHubManager(token)
            user = await github.get_user()
            
            auth_manager.save_token(message.from_user.id, token)
            await message.reply_text(
                f"✅ Successfully logged in as {user['login']}!\n"
                "You can now use all bot commands."
            )
        except Exception as e:
            await message.reply_text("❌ Invalid GitHub token. Please check and try again.")

    @staticmethod
    async def logout_command(client: Client, message: Message):
        auth_manager.remove_token(message.from_user.id)
        await message.reply_text("🔓 Logged out successfully!")

    @staticmethod
    async def create_repo(client: Client, message: Message):
        token = auth_manager.get_token(message.from_user.id)
        if not token:
            await message.reply_text("⚠️ Please login first using /login [token]")
            return

        try:
            args = message.text.split(maxsplit=2)
            if len(args) < 2:
                await message.reply_text("Usage: /create_repo [name] [description]")
                return

            name = args[1]
            description = args[2] if len(args) > 2 else ""
            
            github = GitHubManager(token)
            result = await github.create_repository(name, description)
            
            if result["success"]:
                await message.reply_text(
                    f"✅ Repository created successfully!\n"
                    f"🔗 URL: {result['url']}"
                )
            else:
                await message.reply_text(f"❌ Failed: {result['error']}")
                
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    @staticmethod
    async def list_repos(client: Client, message: Message):
        token = auth_manager.get_token(message.from_user.id)
        if not token:
            await message.reply_text("⚠️ Please login first using /login [token]")
            return

        try:
            github = GitHubManager(token)
            repos = await github.list_repositories()
            
            if not repos:
                await message.reply_text("📚 You don't have any repositories yet.")
                return

            text = "📚 Your Repositories:\n\n"
            for repo in repos:
                text += f"• {repo['name']}\n"
                text += f"  {repo['html_url']}\n\n"

            await message.reply_text(text)
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    @staticmethod
    async def upload_zip(client: Client, message: Message):
        token = auth_manager.get_token(message.from_user.id)
        if not token:
            await message.reply_text("⚠️ Please login first using /login [token]")
            return

        try:
            if not message.reply_to_message or not message.reply_to_message.document:
                await message.reply_text("📎 Please reply to a zip file!")
                return

            doc = message.reply_to_message.document
            if not doc.file_name.endswith('.zip'):
                await message.reply_text("📎 Please send a zip file!")
                return

            status_msg = await message.reply_text("⏳ Downloading zip file...")
            
            github = GitHubManager(token)
            zip_path = await client.download_media(doc)
            await status_msg.edit_text("📂 Extracting files...")
            
            files = await github.extract_zip(zip_path)
            repos = await github.list_repositories()

            # Create inline keyboard with repository options
            buttons = []
            for repo in repos[:10]:  # Limit to 10 repos to avoid button limit
                buttons.append([InlineKeyboardButton(
                    repo['name'],
                    callback_data=f"upload_{repo['name']}"
                )])

            await status_msg.edit_text(
                f"📁 Found {len(files)} files.\n"
                "Select repository to upload to:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    @staticmethod
    async def search_repos(client: Client, message: Message):
        token = auth_manager.get_token(message.from_user.id)
        if not token:
            await message.reply_text("⚠️ Please login first using /login [token]")
            return

        try:
            query = message.text.split(maxsplit=1)[1]
            github = GitHubManager(token)
            results = await github.search_repositories(query)

            if not results:
                await message.reply_text("🔍 No repositories found.")
                return

            text = f"🔍 Search Results for '{query}':\n\n"
            for repo in results[:10]:  # Limit to 10 results
                text += f"• {repo['full_name']}\n"
                text += f"  {repo['html_url']}\n"
                text += f"  ⭐ {repo['stargazers_count']} | 👁 {repo['watchers_count']}\n\n"

            await message.reply_text(text)
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    @staticmethod
    async def create_issue(client: Client, message: Message):
        token = auth_manager.get_token(message.from_user.id)
        if not token:
            await message.reply_text("⚠️ Please login first using /login [token]")
            return

        try:
            args = message.text.split(maxsplit=3)
            if len(args) < 4:
                await message.reply_text(
                    "Usage: /create_issue [repo] [title] [body]\n"
                    "Example: /create_issue my-repo 'Bug report' 'Description here'"
                )
                return

            repo_name = args[1]
            title = args[2]
            body = args[3]

            github = GitHubManager(token)
            result = await github.create_issue(repo_name, title, body)

            if result["success"]:
                await message.reply_text(
                    f"✅ Issue created successfully!\n"
                    f"🔗 URL: {result['url']}"
                )
            else:
                await message.reply_text(f"❌ Failed: {result['error']}")

        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    @staticmethod
    async def list_issues(client: Client, message: Message):
        token = auth_manager.get_token(message.from_user.id)
        if not token:
            await message.reply_text("⚠️ Please login first using /login [token]")
            return

        try:
            repo_name = message.text.split(maxsplit=1)[1]
            github = GitHubManager(token)
            issues = await github.list_issues(repo_name)

            if not issues:
                await message.reply_text("📝 No issues found in this repository.")
                return

            text = f"📝 Issues in {repo_name}:\n\n"
            for issue in issues:
                text += f"#{issue['number']} {issue['title']}\n"
                text += f"Status: {issue['state']}\n"
                text += f"🔗 {issue['html_url']}\n\n"

            await message.reply_text(text)
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    @staticmethod
    async def fork_repo(client: Client, message: Message):
        token = auth_manager.get_token(message.from_user.id)
        if not token:
            await message.reply_text("⚠️ Please login first using /login [token]")
            return

        try:
            repo_full_name = message.text.split(maxsplit=1)[1]
            github = GitHubManager(token)
            result = await github.fork_repository(repo_full_name)

            if result["success"]:
                await message.reply_text(
                    f"✅ Repository forked successfully!\n"
                    f"🔗 URL: {result['url']}"
                )
            else:
                await message.reply_text(f"❌ Failed: {result['error']}")

        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")