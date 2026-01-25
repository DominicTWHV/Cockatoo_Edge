CREATE TABLE IF NOT EXISTS `url_cache` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,

  `url` TEXT NOT NULL,

  `url_hash` VARCHAR(64) NOT NULL,

  `times_seen` INT DEFAULT 1, -- how many times this url has been seen by core

  `parent_set_name` VARCHAR, -- the dataset this url originated from
  
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);

CREATE TABLE IF NOT EXISTS `file_hash_cache` (
  `sha256` VARCHAR PRIMARY KEY,

  `parent_set_name` VARCHAR, -- the dataset this url originated from

  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);

CREATE TABLE IF NOT EXISTS `invite_cache` (
  `invite` VARCHAR PRIMARY KEY, -- will be a argon2id hash

  `parent_set_name` VARCHAR, -- the dataset this url originated from

  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);