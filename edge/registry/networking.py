class SessionConfigs:
    #connection timeout, in seconds, time to wait to establish a connection before timing out
    conn_timeout = 10

    #read timeout, in seconds, for when no data is received before timing out
    read_timeout = 10

    #define pool size, usually 10 is sufficient
    max_connections = 10

    #should exceptions be raised for bad status codes?
    raise_for_status = True

    #enable max file limit protection, to prevent downloading files that are too large and storing them in memory
    dos_protection = True
    max_file_size = 5 * 1024 * 1024  # 5 MB should be sufficient for most files

class UserAgents:
    #declare identity to websites when connecting
    primary = "aiohttp (compatible; CockatooEdge/1.0; +https://github.com/DominicTWHV/Cockatoo_Edge; dataset-download)"

class DatasetDownloadConfigs:
    
    # this is a protection mechanism to avoid downloading files that are not in the allowed mime types
    # recommended to keep enabled unless you have a specific reason to not enable it.
    # when enabled, Cockatoo will perform an automated check of the file type based on the mime type header to ensure it matches expected types.
    # not foolproof, always use caution when downloading files from untrusted sources.
    validate_file_type = True

    allowed_mime_types = [
        "application/json", #Cockatoo Core dataset format are in JSON
        "text/plain", #generic filtering lists are usually txt based
    ]

    read_chunk_size = 1024 #1 KB chunk size for reading files

class FileSourceIdentConfigs:

    #some github domains that may be used for file hosting, excluded gist and githubusercontent
    github_domains = [
        "github.com",
        "www.github.com"
    ]