class PrimaryDBConf:
    sqlite_db_path = "edge/database/sqlite/primary.db"
    sqlite_schema_path = "edge/database/schema/primary.sql"

class SecurityDBConf:
    sqlite_schema_path = "edge/database/schema/security.sql"

    # db path will be dynamically adjusted based on the dataset repository on GitHub.