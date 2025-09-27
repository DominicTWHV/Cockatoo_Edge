CREATE TABLE IF NOT EXISTS `dataset_metadata` (
    `repository` VARCHAR, -- github repository, ex: DominicTWHV/CTI-DB-DUMP | If using a txt dataset, the url will be stored if the dataset isn't on github.
    `licensing` VARCHAR, -- dataset licensing
    `dataset_type` VARCHAR, -- cockatoo_core, text (like traditional url blocklists)
    `remote_update_interval` INT, -- in hours, how often the remote updates

    `num_of_url_entries` INT,
    `num_of_file_entries` INT,
    `num_of_invite_entries` INT,

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `url_cache` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,

  `url` TEXT NOT NULL,

  `url_hash` VARCHAR(64) NOT NULL,

  `times_seen` INT DEFAULT 1, -- how many times this url has been seen by core
  
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);

CREATE TABLE IF NOT EXISTS `file_hash_cache` (
  `sha256` VARCHAR PRIMARY KEY,

  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);

CREATE TABLE IF NOT EXISTS `invite_cache` (
  `invite` VARCHAR PRIMARY KEY, -- will be a sha256 hash

  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);