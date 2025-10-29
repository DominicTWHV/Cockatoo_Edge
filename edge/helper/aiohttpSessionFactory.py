import aiohttp

from edge.registry.networking import SessionConfigs, UserAgents

from edge.logger.context import networking_logger

class SessionFactory:

    _instance = None
    #define a singleton class to prevent initialization in multiple places
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionFactory, cls).__new__(cls)
            cls._instance.session = None

        return cls._instance

    async def create_session(self) -> aiohttp.ClientSession:
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
            self.session = session
            return session
            
        except Exception as e:
            networking_logger.error(f"Failed to create aiohttp ClientSession: {str(e)}")
            raise

    async def grab_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            networking_logger.warning("aiohttp ClientSession is not initialized or closed. Creating a new session.")
            return await self.create_session()
        
        return self.session

    async def close_session(self) -> None:
        try:
            await self.session.close()
            networking_logger.info("Closed aiohttp ClientSession successfully.")
            
        except Exception as e:
            networking_logger.error(f"Failed to close aiohttp ClientSession: {str(e)}")
            raise