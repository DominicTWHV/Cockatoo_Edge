import magic # file type identification\
import tldextract #domain extraction

from edge.helper.downloadMgr import URLParser, DownloadManager
from edge.helper.aiohttpSessionFactory import SessionFactory

from edge.logger.context import networking_logger

from edge.registry.networking import DatasetDownloadConfigs, FileSourceIdentConfigs

class Ident:

    @staticmethod
    async def remote_file_type(url: str) -> str:
        session = await SessionFactory().grab_session()
        async with session.get(url) as response:
            mime_header = response.headers.get('Content-Type', '').lower()

            chunk = await response.content.read(DatasetDownloadConfigs.read_chunk_size)  #read a certain amount of bytes for identification

            detected_type = magic.from_buffer(chunk, mime=True) #json, text/plain, etc.

            networking_logger.debug(f"File Type Identification: Detected type: {detected_type}, Mime Header: {mime_header}")

            return detected_type, mime_header
        
    @staticmethod
    async def file_source(url: str) -> str:
        extracted = tldextract.extract(url)
        
        domain = extracted.registered_domain.lower()

        if domain in FileSourceIdentConfigs.github_domains:
            networking_logger.debug(f"URL {url} identified as GitHub domain: {domain}")
            return "github"
        
        networking_logger.debug(f"URL {url} source is non-GitHub domain: {domain}")
        return "unknown"
    
class Verify:

    @staticmethod
    async def file_type_allowed(detected_type: str) -> bool:
        if not DatasetDownloadConfigs.validate_file_type:
            networking_logger.debug(f"File Type Verification: Validation disabled. Bypassing checks. File type: {detected_type}")
            return True

        if detected_type in DatasetDownloadConfigs.allowed_mime_types:
            networking_logger.info(f"File Type Verification: Detected type {detected_type} is allowed.")
            return True
        
        else:
            networking_logger.warning(f"File Type Verification: Detected type {detected_type} is NOT allowed.")
            return False
    
class DSDownload:

    @staticmethod
    async def pipeline(url: str) -> str:
        detected_type, mime_header = await Ident.remote_file_type(url)
        source = await Ident.file_source(url)

        if not await Verify.file_type_allowed(detected_type):
            networking_logger.error(f"Dataset Download Pipeline: File type {detected_type} not allowed. Aborting download for safety. URL: {url}")
            return
        
        if source == "github": #parse out the raw github content url (raw.githubusercontent.com links will NOT be identified as github)
            raw_url = await URLParser.parse_github_url(url)
            url = raw_url.append("metadata.json") #append the standard dataset filename for Cockatoo Core dataset format

            content = await DownloadManager.download_file(url) #download the mnetadata file into a variable

        else:
            content = await DownloadManager.download_file(url) # -> this is the set as not using cockatoo core dataset format