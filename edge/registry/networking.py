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
    max_file_size = 2 * 1024 * 1024  # 2 MB should be sufficient for most files

class UserAgents:
    #declare identity to websites when connecting
    primary = "aiohttp (compatible; CockatooEdge/1.0; +https://github.com/DominicTWHV/Cockatoo_Edge; dataset-download)"