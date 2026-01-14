import magic # file type identification\
import tldextract #domain extraction
import json

from edge.helper.downloadMgr import URLParser, DownloadManager
from edge.helper.aiohttpSessionFactory import SessionFactory

from edge.logger.context import networking_logger

from edge.registry.networking import DatasetDownloadConfigs, FileSourceIdentConfigs
from edge.registry.dataStructure import CoreDatasetMetadata
from edge.registry.dataset import SetDownload

class Ident:

    @staticmethod
    async def remote_file_type(url: str) -> str:
        #identifies the file type of a remote file by reading a chunk of it
        
        session = await SessionFactory().grab_session()
        async with session.get(url) as response:
            mime_header = response.headers.get('Content-Type', '').lower()

            chunk = await response.content.read(DatasetDownloadConfigs.read_chunk_size)  #read a certain amount of bytes for identification

            detected_type = magic.from_buffer(chunk, mime=True) #json, text/plain, etc.

            networking_logger.debug(f"File Type Identification: Detected type: {detected_type}, Mime Header: {mime_header}")

            return detected_type, mime_header
        
    @staticmethod
    async def file_source(url: str) -> str:
        #determines if the url is from github or not

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
    async def pipeline(url: str) -> dict:
        """
        Main pipeline for downloading datasets from various sources.
        Supports both GitHub Cockatoo Core format and generic text URLs.
        
        Returns:
            dict: Status information with 'success', 'source', 'file_count', and 'message'
        """
        try:
            detected_type, mime_header = await Ident.remote_file_type(url)
            source = await Ident.file_source(url)

            if not await Verify.file_type_allowed(detected_type):
                networking_logger.error(f"Dataset Download Pipeline: File type {detected_type} not allowed. Aborting download for safety. URL: {url}")
                return {"success": False, "source": source, "file_count": 0, "message": f"File type {detected_type} not allowed"}
            
            if source == "github":
                return await DSDownload.github_download(url)
            
            else:
                return await DSDownload.generic_download(url)
                
        except Exception as e:
            networking_logger.error(f"Dataset Download Pipeline: Error occurred - {str(e)}")
            return {"success": False, "source": "unknown", "file_count": 0, "message": str(e)}

    @staticmethod
    async def github_download(url: str) -> dict:
        #expects a root github repo url

        try:
            # Parse out the raw github content url
            raw_url = await URLParser.parse_github_url(url)
            metadata_url = f"{raw_url}/metadata.json"

            networking_logger.info(f"GitHub Download: Fetching metadata from {metadata_url}")
            
            # Download and parse metadata file
            metadata_content_raw = await DownloadManager.download_file(metadata_url)
            metadata_content = json.loads(metadata_content_raw)

            # Get the list of relevant files from metadata
            relevent_files = metadata_content.get(CoreDatasetMetadata.relevent_files, [])
            
            if not relevent_files:
                networking_logger.warning(f"GitHub Download: No relevant files found in metadata")
                return {"success": False, "source": "github", "file_count": 0, "message": "No relevant files in metadata"}

            networking_logger.info(f"GitHub Download: Found {len(relevent_files)} files in metadata")

            # Remove unnecessary files from the list
            for file_to_remove in SetDownload.removed_files:
                if file_to_remove in relevent_files:
                    relevent_files.remove(file_to_remove)
                    networking_logger.debug(f"GitHub Download: Removed {file_to_remove} from download list")

            # Download each relevant file
            downloaded_count = 0
            for file_to_download in relevent_files:
                try:
                    file_url = f"{raw_url}/{file_to_download}"
                    networking_logger.debug(f"GitHub Download: Downloading {file_to_download} from {file_url}")
                    
                    content = await DownloadManager.download_file(file_url)
                    json_content = json.loads(content)

                    # Process the downloaded content (store in database, etc.)
                    await DSDownload._process_dataset_content(json_content, file_to_download, "github")
                    downloaded_count += 1
                    networking_logger.info(f"GitHub Download: Successfully processed {file_to_download}")
                    
                except json.JSONDecodeError:
                    networking_logger.error(f"GitHub Download: Failed to parse JSON from {file_to_download}")

                except Exception as e:
                    networking_logger.error(f"GitHub Download: Error downloading {file_to_download}: {str(e)}")

            networking_logger.info(f"GitHub Download: Completed. Downloaded and processed {downloaded_count}/{len(relevent_files)} files")
            return {
                "success": downloaded_count > 0,
                "source": "github",
                "file_count": downloaded_count,
                "message": f"Successfully downloaded {downloaded_count} files"
            }
            
        except Exception as e:
            networking_logger.error(f"GitHub Download: Pipeline error - {str(e)}")
            return {"success": False, "source": "github", "file_count": 0, "message": str(e)}

    @staticmethod
    async def generic_download(url: str) -> dict:
        """
        Download generic datasets from any URL (typically plain text format).
        
        Returns:
            dict: Status information with 'success', 'source', 'file_count', and 'message'
        """
        try:
            networking_logger.info(f"Generic Download: Starting download from {url}")
            
            content = await DownloadManager.download_file(url)
            
            if not content:
                networking_logger.warning(f"Generic Download: No content received from {url}")
                return {"success": False, "source": "unknown", "file_count": 0, "message": "No content received"}

            # process the downloaded content (store in database, etc.)
            await DSDownload._process_dataset_content(content, url, "generic")
            
            networking_logger.info(f"Generic Download: Successfully downloaded and processed content from {url}")
            return {
                "success": True,
                "source": "unknown",
                "file_count": 1,
                "message": "Successfully downloaded generic dataset"
            }
            
        except Exception as e:
            networking_logger.error(f"Generic Download: Error - {str(e)}")
            return {"success": False, "source": "unknown", "file_count": 0, "message": str(e)}

    @staticmethod
    async def _process_dataset_content(content, source_identifier: str, source_type: str) -> None:
        """
        Internal method to process downloaded dataset content.
        Handles storage to database or other processing as needed.
        
        Args:
            content: The downloaded content (dict for JSON, str for text)
            source_identifier: Filename or URL identifier
            source_type: 'github' or 'generic'
        """
        try:
            networking_logger.debug(f"Processing dataset from {source_type} source: {source_identifier}")
            
            # TODO: Implement actual storage logic to database
            
            networking_logger.debug(f"Dataset content processed: {source_identifier}")
            
        except Exception as e:
            networking_logger.error(f"Error processing dataset content from {source_identifier}: {str(e)}")
            raise