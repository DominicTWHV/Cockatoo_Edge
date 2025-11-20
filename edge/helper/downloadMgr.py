from edge.logger.context import networking_logger

from edge.helper.aiohttpSessionFactory import SessionFactory

from edge.registry.networking import SessionConfigs
from edge.registry.exceptions import DownloadSizeExceededError

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
    
    @staticmethod
    async def download_file(url: str, dos_protection: bool = SessionConfigs.dos_protection, max_size: int = SessionConfigs.max_file_size) -> str:
        session = SessionFactory().grab_session()
        async with session.get(url) as response:

            if SessionConfigs.raise_for_status:
                response.raise_for_status()

            body = []
            downloaded = 0

            try:
                async for chunk in response.content.iter_chunked(8192):
                    if not isinstance(chunk, (bytes, bytearray)):
                        # Safety net (shouldn't happen with iter_chunked)
                        continue

                    chunk_len = len(chunk)
                    downloaded += chunk_len

                    if dos_protection and downloaded > max_size:
                        raise DownloadSizeExceededError(f"Downloaded content too large: {downloaded} bytes (limit: {max_size} bytes)")

                    #incremental decode to handle file streaming -> avoid DoS with large text files
                    body.append(chunk.decode(response.get_encoding()))

            except Exception as e:
                networking_logger.error(f"Download Manager: Error downloading file from {url}: {e}")
                return ""

            return "".join(body)