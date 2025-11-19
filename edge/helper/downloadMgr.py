from edge.logger.context import networking_logger

from edge.helper.aiohttpSessionFactory import SessionFactory

class URLParser:

    @staticmethod
    async def parse_github_url(url: str, branch: str = "main") -> str:
        if "github.com" not in url:
            networking_logger.error(f"GitHub Parser: URL is not a GitHub URL: {url}")
            return ""

        parts = url.split('/')
        if len(parts) < 5:
            networking_logger.error(f"GitHub Parser: Invalid GitHub URL format: {url}")
            return ""

        user = parts[3]
        repo = parts[4]

        if repo.endswith('.git'): #remove the .git suffix
            repo = repo[:-4]

        if "tree" in parts:
            branch_index = parts.index("tree") + 1
            if branch_index < len(parts):
                branch = parts[branch_index]
        
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/" #return a raw github url for easier file download.

        networking_logger.info(f"GitHub Parser: Parsed GitHub link to raw URL: {raw_url}")

        return raw_url

class DownloadManager:
    
    async def download_file(self, url: str) -> str:
        session = SessionFactory().grab_session()
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            return content