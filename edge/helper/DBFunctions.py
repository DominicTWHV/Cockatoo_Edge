from typing import Any

from edge.helper.cryptography import SHA256

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

class MetadataDB:
    def __init__(self):
        self.db = SQLiteDriver(MetadataDBConf.sqlite_db_path) #initialize class as the metadata database

    #===================================================================

    # fetch a list of primary keys
    async def fetch_prim_keys(self, table: str) -> list:
        return await self.db.fetch_all_keys(table)
    
    # wipes table
    async def wipe_table(self, table: str) -> bool:
        return await self.db.wipe_etable(table)
    
    #===================================================================

    async def update_dataset_metadata(self, repository:str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        repository_hash = await SHA256.generate(repository)

        if "repository_url" not in entry_names: # ensure repository url is always stored
            entry_names.append("repository_url")
            entry_values.append(repository)
        
        return await self.db.ins_w_key("dataset_metadata", "repository_hash", repository_hash, entry_names, entry_values) #update or insert new metadata specific repository
    
    async def fetch_dataset_metadata(self, repository: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        repository_hash = await SHA256.generate(repository)
        return await self.db.fetch_w_key("dataset_metadata", "repository_hash", repository_hash)
    
    async def delete_dataset_metadata(self, repository: str) -> bool: # deletes metadata for a specific repository
        repository_hash = await SHA256.generate(repository)
        return await self.db.wipe_w_key("dataset_metadata", "repository_hash", repository_hash)
    
    #===================================================================
    
    async def update_dataset(self, repository:str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        repository_hash = await SHA256.generate(repository)

        if "repository_url" not in entry_names: # ensure repository url is always stored
            entry_names.append("repository_url")
            entry_values.append(repository)

        return await self.db.ins_w_key("datasets", "repository_hash", repository_hash, entry_names, entry_values) #update or insert new dataset specific repository
    
    async def fetch_dataset(self, repository: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        repository_hash = await SHA256.generate(repository)
        return await self.db.fetch_w_key("datasets", "repository_hash", repository_hash)
    
    async def delete_dataset(self, repository: str) -> bool: # deletes dataset for a specific repository
        repository_hash = await SHA256.generate(repository)
        return await self.db.wipe_w_key("datasets", "repository_hash", repository_hash)
    
class PrimaryDB:
    def __init__(self):
        self.db = SQLiteDriver(PrimaryDBConf.sqlite_db_path) #initialize class as the primary database

    #===================================================================

    # fetch a list of primary keys
    async def fetch_prim_keys(self, table: str) -> list:
        return await self.db.fetch_all_keys(table)
    
    # wipes table
    async def wipe_table(self, table: str) -> bool:
        return await self.db.wipe_etable(table)
    
    #===================================================================

    async def update_configs(self, server_id: int, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        return await self.db.ins_w_key("configs", "server_id", server_id, entry_names, entry_values) #update or insert new config for specific server
    
    async def fetch_configs(self, server_id: int) -> list: # fetches a list of stored values, if doesn't exist, will return []
        return await self.db.fetch_w_key("configs", "server_id", server_id)
    
    async def delete_configs(self, server_id: int) -> bool: # deletes config for a specific server
        return await self.db.wipe_w_key("configs", "server_id", server_id)
    
    #===================================================================
    
    async def update_moderation_logs(self, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        return await self.db.special_ins_w_uid("moderation_logs", entry_names, entry_values) #insert new moderation log
    
    async def fetch_moderation_logs(self, entry_id: int) -> list:
        return await self.db.fetch_w_key("moderation_logs", "id", entry_id)
    
    # should NOT be used normally, but leaving it here for completeness (the code does not reference this function)
    async def delete_moderation_logs(self, entry_id: int) -> bool: # deletes moderation log by id
        return await self.db.wipe_w_key("moderation_logs", "id", entry_id)
    
class SecurityGenericDB:
    def __init__(self):
        self.db = SQLiteDriver(SecurityDBConf.sqlite_db_path_generic) #initialize class as the security generic database

    #===================================================================

    # fetch a list of primary keys
    async def fetch_prim_keys(self, table: str) -> list:
        return await self.db.fetch_all_keys(table)
    
    # wipes table
    async def wipe_table(self, table: str) -> bool:
        return await self.db.wipe_etable(table)
    
    #===================================================================

    async def update_generic_url_cache(self, url: str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        url_hash = await SHA256.generate(url)

        if "url" not in entry_names: # ensure url is always stored
            entry_names.append("url")
            entry_values.append(url)
        
        return await self.db.ins_w_key("url_cache", "url_hash", url_hash, entry_names, entry_values, True) #update or insert new generic url cache entry (silenced)
    
    async def fetch_generic_url_cache(self, url: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        url_hash = await SHA256.generate(url)
        return await self.db.fetch_w_key("url_cache", "url_hash", url_hash)
    
    async def delete_generic_url_cache(self, url: str) -> bool: # deletes generic url cache entry
        url_hash = await SHA256.generate(url)
        return await self.db.wipe_w_key("url_cache", "url_hash", url_hash)
    
    #===================================================================
    
    async def update_generic_file_cache(self, file_hash: str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        return await self.db.ins_w_key("file_hash_cache", "sha256", file_hash, entry_names, entry_values, True) #update or insert new generic file cache entry (silenced)
    
    async def fetch_generic_file_cache(self, file_hash: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        return await self.db.fetch_w_key("file_hash_cache", "sha256", file_hash)
    
    async def delete_generic_file_cache(self, file_hash: str) -> bool: # deletes generic file cache entry
        return await self.db.wipe_w_key("file_hash_cache", "sha256", file_hash)
    
    #===================================================================
    
    async def update_invite_cache(self, invite: str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        #note: the invite field is an argon2id hash of the original invite
        
        return await self.db.ins_w_key("invite_cache", "invite", invite, entry_names, entry_values, True) #update or insert new invite cache entry (silenced)
    
    async def fetch_invite_cache(self, invite: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        return await self.db.fetch_w_key("invite_cache", "invite", invite)
    
    async def delete_invite_cache(self, invite: str) -> bool: # deletes invite cache entry
        return await self.db.wipe_w_key("invite_cache", "invite", invite)
    
class SecurityCoreDB:

    def __init__(self):
        self.db = SQLiteDriver(SecurityDBConf.sqlite_db_path_core) #initialize class as the security core database

    #===================================================================

    # fetch a list of primary keys
    async def fetch_prim_keys(self, table: str) -> list:
        return await self.db.fetch_all_keys(table)
    
    # wipes table
    async def wipe_table(self, table: str) -> bool:
        return await self.db.wipe_etable(table)
    
    #===================================================================

    async def update_core_url_cache(self, url: str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        url_hash = await SHA256.generate(url)

        if "url" not in entry_names: # ensure url is always stored
            entry_names.append("url")
            entry_values.append(url)
        
        return await self.db.ins_w_key("url_cache", "url_hash", url_hash, entry_names, entry_values, True) #update or insert new core url cache entry (silenced)
    
    async def fetch_core_url_cache(self, url: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        url_hash = await SHA256.generate(url)
        return await self.db.fetch_w_key("url_cache", "url_hash", url_hash)
    
    async def delete_core_url_cache(self, url: str) -> bool: # deletes core url cache entry
        url_hash = await SHA256.generate(url)
        return await self.db.wipe_w_key("url_cache", "url_hash", url_hash)
    
    #===================================================================

    async def update_core_file_cache(self, file_hash: str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        return await self.db.ins_w_key("file_hash_cache", "sha256", file_hash, entry_names, entry_values, True) #update or insert new core file cache entry (silenced)
    
    async def fetch_core_file_cache(self, file_hash: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        return await self.db.fetch_w_key("file_hash_cache", "sha256", file_hash)
    
    async def delete_core_file_cache(self, file_hash: str) -> bool: # deletes core file cache entry
        return await self.db.wipe_w_key("file_hash_cache", "sha256", file_hash)
    
    #===================================================================

    async def update_core_invite_cache(self, invite: str, entry_names: list[str], entry_values: list[Any]) -> bool:
        if len(entry_names) != len(entry_values):
            raise ValueError("Entry names and values lists must be of the same length")
        
        #note: the invite field is an argon2id hash of the original invite
        
        return await self.db.ins_w_key("invite_cache", "invite", invite, entry_names, entry_values, True) #update or insert new invite cache entry (silenced)
    
    async def fetch_core_invite_cache(self, invite: str) -> list: # fetches a list of stored values, if doesn't exist, will return []
        return await self.db.fetch_w_key("invite_cache", "invite", invite)
    
    async def delete_core_invite_cache(self, invite: str) -> bool: # deletes invite cache entry
        return await self.db.wipe_w_key("invite_cache", "invite", invite)