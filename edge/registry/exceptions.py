class DownloadSizeExceededError(Exception):
    # raised when aiohttp download stream exceeds maximum allowed file size
    pass