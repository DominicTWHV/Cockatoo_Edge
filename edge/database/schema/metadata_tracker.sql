CREATE TABLE IF NOT EXISTS `dataset_metadata` (
    `repository` VARCHAR, -- github repository, ex: DominicTWHV/CTI-DB-DUMP | If using a txt dataset, the url will be stored if the dataset isn't on github.
    `licensing` VARCHAR, -- dataset licensing
    `dataset_type` VARCHAR, -- cockatoo_core, text (like traditional url blocklists)
    `remote_update_interval` INT, -- in hours, how often the remote updates

    `num_of_url_entries` INT,
    `num_of_file_entries` INT,
    `num_of_invite_entries` INT,

    `enabled` INT DEFAULT 0, -- whether this dataset is enabled (1 = true, 0 = false)

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);