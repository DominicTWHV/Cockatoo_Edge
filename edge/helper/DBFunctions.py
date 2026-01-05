import hashlib

from typing import Any

from edge.database.driver import SQLiteDriver, DBInitManager

from edge.registry.database import PrimaryDBConf, SecurityDBConf, MetadataDBConf

class AutoDBMgr:
    
    @staticmethod
    async def init_db() -> None: #initializes static db instances. Not used for dataset dbs

        for db_path, db_type in [
            (PrimaryDBConf.sqlite_db_path, "primary"),
            (SecurityDBConf.sqlite_db_path_core, "security_core"),
            (SecurityDBConf.sqlite_db_path_generic, "security_generic"),
            (MetadataDBConf.sqlite_db_path, "metadata"),
            
        ]:
            await DBInitManager.init_db(db_type=db_type, db_path=db_path)