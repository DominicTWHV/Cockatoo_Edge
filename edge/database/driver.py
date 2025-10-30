import os

import aiosqlite
import aiofiles

from typing import Literal, Any

from edge.logger.context import db_logger

from edge.registry.database import PrimaryDBConf, SecurityDBConf

class DBInitManager:
    @staticmethod
    async def init_db(db_type: Literal["primary", "security_core", "security_generic"], db_path: str = PrimaryDBConf.sqlite_db_path) -> None: #expandable support for multiple dbs

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
    async def _init_sqlite(db_type: Literal["primary", "security_core", "security_generic"], db_path: str) -> None: # need to explicitly define security db path
        config_map = {
            "primary": (PrimaryDBConf.sqlite_schema_path),
            "security_core": (SecurityDBConf.sqlite_schema_path_core),
            "security_generic": (SecurityDBConf.sqlite_schema_path_generic),
        }
        
        schema_path = config_map[db_type]
        
        async with aiosqlite.connect(db_path) as db:
            async with aiofiles.open(schema_path, mode='r') as file:
                schema_sql = await file.read()
            await db.executescript(schema_sql)
            await db.commit()

class SQLiteDriver:
    def __init__(self, path: str = PrimaryDBConf.sqlite_db_path) -> None:
        self.db_path = path

    async def ins_w_key(self, table_name: str, key_col: str, key_val: Any, columns: list[str], values: list[Any], silence: bool = False) -> bool:
        # insert or update a row identified by the primary key.

        if len(columns) != len(values):
            return False

        try:
            async with aiosqlite.connect(self.db_path) as db:
                all_columns = [key_col] + columns
                all_values = [key_val] + values
                placeholders = ", ".join("?" for _ in all_columns)
                col_clause = ", ".join(all_columns)
                update_clause = ", ".join(f"{col} = excluded.{col}" for col in columns)
                
                await db.execute(
                    "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT({}) DO UPDATE SET {}".format(
                        table_name, col_clause, placeholders, key_col, update_clause
                    ),
                    all_values
                )
                await db.commit()
                if not silence:
                    db_logger.info(f"SQLite: Inserted/Updated row in {table_name} with key column {key_col} value {key_val}")
                
                return True
            
        except Exception as e:
            db_logger.error(f"SQLite: Failed to insert/update row in {table_name} with key column {key_col} value {key_val}: Error: {str(e)}")
            return False

    async def ins_wo_key(self, table_name: str, columns: list[str], values: list[Any], silence: bool = False) -> bool:
        # insert or update a row without a primary key.

        if len(columns) != len(values):
            return False

        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = (await cursor.fetchone())[0]
                await cursor.close()

                if row_count == 0:
                    placeholders = ", ".join("?" for _ in columns)
                    col_clause = ", ".join(columns)
                    
                    await db.execute(
                        f"INSERT INTO {table_name} ({col_clause}) VALUES ({placeholders})",
                        values
                    )
                else:
                    update_clause = ", ".join(f"{col} = ?" for col in columns)
                    
                    await db.execute(
                        f"UPDATE {table_name} SET {update_clause}",
                        values
                    )
                
                await db.commit()
                if not silence:
                    db_logger.info(f"SQLite: Inserted/Updated row in {table_name} without key column")

                return True
            
        except Exception as e:
            db_logger.error(f"SQLite: Failed to insert/update row in {table_name} without key column: Error: {str(e)}")
            return False

    async def wipe_w_key(self, table_name: str, key_col: str, key_val: Any, silence: bool = False) -> bool:
        # delete the row identified by the primary key to remove the empty null row

        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    f"DELETE FROM {table_name} WHERE {key_col} = ?",
                    (key_val,)
                )
                await db.commit()
                if not silence:
                    db_logger.info(f"SQLite: Wiped row in {table_name} with key column {key_col} value {key_val}")
                
                return True
            
        except Exception as e:
            db_logger.error(f"SQLite: Failed to wipe row in {table_name} with key column {key_col} value {key_val}: Error: {str(e)}")
            return False

    async def wipe_wo_key(self, table_name: str, columns: list[str], silence: bool = False) -> bool:
        # wipe specific columns in the table by setting them to NULL.
        if not columns:
            return False

        try:
            set_clause = ", ".join(f"{col} = NULL" for col in columns)
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    f"UPDATE {table_name} SET {set_clause}"
                )
                await db.commit()
                if not silence:
                    db_logger.info(f"SQLite: Wiped columns {columns} in {table_name} without key column")
                
                return True
            
        except Exception as e:
            db_logger.error(f"SQLite: Failed to wipe columns {columns} in {table_name}: Error: {str(e)}")
            return False

    async def fetch_w_key(self, table_name: str, key_col: str, key_val: Any, silence: bool = False) -> list:
        #fetch the entire row identified by the primary key.
        try:
            async with aiosqlite.connect(self.db_path) as db:
                #fetch the first row matching the key.
                cursor = await db.execute(
                    f"SELECT * FROM {table_name} WHERE {key_col} = ? LIMIT 1",
                    (key_val,)
                )
                row = await cursor.fetchone()
                await cursor.close()

                if row is not None:
                    if not silence:
                        db_logger.info(f"SQLite: Fetched row in {table_name} with key column {key_col} value {key_val}")
                    # return the row's values as a list. Specific NULLs are kept as None.

                    return list(row)
                
                else:
                    return []
                
        except Exception as e:
            db_logger.error(f"SQLite: Failed to fetch row in {table_name} with key column {key_col} value {key_val}: Error: {str(e)}")
            return False

    async def fetch_wo_key(self, table_name: str, column: str, silence: bool = False) -> list:
        # fetch all values from a specific column in the given table.

        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    f"SELECT {column} FROM {table_name}"
                )
                rows = await cursor.fetchall()
                await cursor.close()

                if not silence:
                    db_logger.info(f"SQLite: Fetched column {column} from {table_name} without key column")
                
                return [row[0] for row in rows]
            
        except Exception as e:
            db_logger.error(f"SQLite: Failed to fetch column {column} from {table_name}: Error: {str(e)}")
            return False

    async def fetch_specific_col_w_key(self, table_name: str, key_col: str, key_val: Any, column: str, silence: bool = False) -> Any:
        # fetch a specific column value from the row identified by the key.
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    f"SELECT {column} FROM {table_name} WHERE {key_col} = ? LIMIT 1",
                    (key_val,)
                )
                row = await cursor.fetchone()
                await cursor.close()

                if row is not None:
                    if not silence:
                        db_logger.info(f"SQLite: Fetched column {column} from {table_name} with key column {key_col} value {key_val}")

                    return row[0]
                
                else:
                    return None
                
        except Exception as e:
            db_logger.error(f"SQLite: Failed to fetch column {column} from {table_name} with key column {key_col} value {key_val}: Error: {str(e)}")
            return False
        
    async def fetch_etable_wo_key(self, table_name: str, silence: bool = False) -> list:
        # fetch one value from each column in the given table.
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # attempt to fetch the first row from the table.
                cursor = await db.execute(f"SELECT * FROM {table_name} LIMIT 1")
                row = await cursor.fetchone()
                await cursor.close()

                if row is not None:
                    return list(row)
                else:
                    # if no rows are found, determine the number of columns.
                    cursor2 = await db.execute(f"PRAGMA table_info({table_name})")
                    columns_info = await cursor2.fetchall()
                    await cursor2.close()

                    if not silence:
                        db_logger.info(f"SQLite: Fetched entire table {table_name} without key column")

                    return [None] * len(columns_info)
                
        except Exception as e:
            db_logger.error(f"SQLite: Failed to fetch an entire table {table_name}: Error: {str(e)}")
            return False

    async def fetch_all_keys(self, table_name: str, silence: bool = False) -> list:
        # get all the primary keys in a table
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # get the primary key column name(s)
                cursor = await db.execute(f"PRAGMA table_info({table_name})")
                columns_info = await cursor.fetchall()
                await cursor.close()
                
                primary_keys = [col[1] for col in columns_info if col[5] > 0]  #col[5] is the pk column
                if not primary_keys:
                    return False
                
                # fetch all primary key values
                key_clause = ", ".join(primary_keys)
                cursor2 = await db.execute(f"SELECT {key_clause} FROM {table_name}")
                rows = await cursor2.fetchall()
                await cursor2.close()

                if not silence:
                    db_logger.info(f"SQLite: Fetched all primary keys from {table_name}")

                return [row[0] for row in rows]
            
        except Exception as e:
            db_logger.error(f"SQLite: Failed to fetch all primary keys from {table_name}: Error: {str(e)}")
            return False
        
    async def wipe_etable(self, table_name: str, silence: bool = False) -> bool:
        # wipe the entire table defined by table_name
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(f"DELETE FROM {table_name}")
                await db.commit()
                if not silence:
                    db_logger.info(f"SQLite: Wiped table {table_name}")

                return True
            
        except Exception as e:
            db_logger.error(f"SQLite: Failed to wipe table {table_name}: Error: {str(e)}")
            return False