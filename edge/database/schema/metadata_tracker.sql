CREATE TABLE IF NOT EXISTS `dataset_metadata` (
    `repository_hash` VARCHAR(64) PRIMARY KEY, -- sha256 hash of the repository url
    `repository_url` VARCHAR, -- url to the repository or txt dataset

    `licensing` VARCHAR, -- dataset licensing
    `dataset_type` VARCHAR, -- cockatoo_core, text (like traditional url blocklists)
    `remote_update_interval` INT, -- in hours, how often the remote updates

    `num_of_url_entries` INT,
    `num_of_file_entries` INT,
    `num_of_invite_entries` INT,

    `enabled` INT DEFAULT 0, -- whether this dataset is enabled (1 = true, 0 = false)

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- this table manages dataset updates
CREATE TABLE IF NOT EXISTS `datasets` (
    `repository_hash` VARCHAR(64) PRIMARY KEY, -- sha256 hash of the repository url
    `repository_url` VARCHAR, -- github repository, ex: https://github.com/DominicTWHV/CTI-DB-DUMP/ | If using a txt dataset, the url will be stored if the dataset isn't on github.

    `auto_update` INT DEFAULT 1, -- whether to auto update the security dataset or not (1 = true, 0 = false)
    `update_interval` INT DEFAULT 0, -- interval to pull in dataset updates in minutes. Use 0 to set the time automatically. If non-zero, this will override the value in dataset_metadata table.

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);