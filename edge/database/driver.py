import os

import aiosqlite
import aiofiles

from typing import Literal, Optional, Any

from edge.logger.context import db_logger

from edge.registry.database import PrimaryDBConf, SecurityDBConf

class DBInitManager:
    @staticmethod
    async def init_db(db_type: Literal["primary", "security"], db_path: str = PrimaryDBConf.sqlite_db_path) -> None: #expandable support for multiple dbs

        db_type = db_type.lower()
        backend = "SQLite (async)"
        
        db_logger.info(f"Initializing database. | Type: {db_type} | Backend: {backend}")
        
        try:
            await DBInitManager._init_sqlite(db_type, db_path)
                
        except Exception as e:
            db_logger.error(f"Error initializing database: {e} | Type: {db_type} | Backend: {backend}\n")
            raise
            
        db_logger.info(f"Database initialized.  | Type: {db_type} | Backend: {backend}\n")
    
    @staticmethod
    async def _init_sqlite(db_type: Literal["primary", "security"], db_path: str) -> None: # need to explicitly define security db path
        config_map = {
            "primary": (PrimaryDBConf.sqlite_schema_path),
            "security": (SecurityDBConf.sqlite_schema_path),
        }
        
        schema_path = config_map[db_type]
        
        async with aiosqlite.connect(db_path) as db:
            async with aiofiles.open(schema_path, mode='r') as file:
                schema_sql = await file.read()
            await db.executescript(schema_sql)
            await db.commit()