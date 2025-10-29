import aiohttp

class DownloadManager:
    
    async def download_file(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                if response.status == 200: #normal response
                    byte_data = await response.read() #download file
                    return byte_data.decode('utf-8') #return as string