import aiohttp

from edge.registry.networking import SessionConfigs, UserAgents
from edge.logger.context import networking_logger

class SessionFactory:

    @staticmethod
    async def create_session() -> aiohttp.ClientSession:
        try:
            #configure timeouts
            timeout = aiohttp.ClientTimeout(
                total=None,
                connect=SessionConfigs.conn_timeout,
                sock_read=SessionConfigs.read_timeout
            )
            
            #create connector with max connections
            connector = aiohttp.TCPConnector(limit=SessionConfigs.max_connections)
            
            #create session with specified configurations
            session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={"User-Agent": UserAgents.primary},
                raise_for_status=SessionConfigs.raise_for_status
            )

            networking_logger.info(f"Created aiohttp ClientSession object with {SessionConfigs.max_connections} connections.")
            return session
            
        except Exception as e:
            networking_logger.error(f"Failed to create aiohttp ClientSession: {str(e)}")
            raise

    @staticmethod
    async def close_session(session: aiohttp.ClientSession) -> None:
        try:
            await session.close()
            networking_logger.info("Closed aiohttp ClientSession successfully.")
            
        except Exception as e:
            networking_logger.error(f"Failed to close aiohttp ClientSession: {str(e)}")
            raise