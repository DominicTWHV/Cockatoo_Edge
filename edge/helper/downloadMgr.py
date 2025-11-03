from edge.helper.aiohttpSessionFactory import SessionFactory

class DownloadManager:
    
    async def download_file(self, url: str) -> str:
        session = SessionFactory().grab_session()
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            return content