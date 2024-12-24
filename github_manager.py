from github import Github
import os
import zipfile
from typing import List, Dict

class GitHubManager:
    def __init__(self, token: str):
        self.github = Github(token)
        self.user = self.github.get_user()

    async def get_user(self) -> Dict:
        """Get authenticated user info"""
        return {
            "login": self.user.login,
            "name": self.user.name,
            "email": self.user.email
        }

    async def create_repository(self, name: str, description: str = "", private: bool = False) -> Dict:
        """Create a new GitHub repository"""
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=True
            )
            return {
                "success": True,
                "url": repo.html_url,
                "name": repo.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def list_repositories(self) -> List[Dict]:
        """List user's repositories"""
        try:
            repos = []
            for repo in self.user.get_repos():
                repos.append({
                    "name": repo.name,
                    "html_url": repo.html_url,
                    "description": repo.description,
                    "private": repo.private
                })
            return repos
        except Exception as e:
            return []

    async def search_repositories(self, query: str) -> List[Dict]:
        """Search GitHub repositories"""
        try:
            results = []
            for repo in self.github.search_repositories(query):
                results.append({
                    "full_name": repo.full_name,
                    "html_url": repo.html_url,
                    "description": repo.description,
                    "stargazers_count": repo.stargazers_count,
                    "watchers_count": repo.watchers_count
                })
            return results
        except Exception as e:
            return []

    async def create_issue(self, repo_name: str, title: str, body: str) -> Dict:
        """Create an issue in a repository"""
        try:
            repo = self.user.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body)
            return {
                "success": True,
                "url": issue.html_url,
                "number": issue.number
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def list_issues(self, repo_name: str) -> List[Dict]:
        """List issues in a repository"""
        try:
            repo = self.user.get_repo(repo_name)
            issues = []
            for issue in repo.get_issues():
                issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "html_url": issue.html_url
                })
            return issues
        except Exception as e:
            return []

    async def fork_repository(self, full_name: str) -> Dict:
        """Fork a repository"""
        try:
            repo = self.github.get_repo(full_name)
            fork = self.user.create_fork(repo)
            return {
                "success": True,
                "url": fork.html_url,
                "name": fork.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def extract_zip(self, zip_path: str, extract_path: str = "./temp") -> List[Dict]:
        """Extract zip file and return file contents"""
        try:
            os.makedirs(extract_path, exist_ok=True)
            files = []
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                
                for root, _, filenames in os.walk(extract_path):
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            relative_path = os.path.relpath(file_path, extract_path)
                            files.append({
                                "path": relative_path,
                                "content": content
                            })
            
            return files
        except Exception as e:
            raise Exception(f"Error extracting zip: {str(e)}")
        finally:
            # Cleanup
            if os.path.exists(extract_path):
                for root, dirs, files in os.walk(extract_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(extract_path)