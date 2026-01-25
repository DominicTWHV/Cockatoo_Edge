CREATE TABLE IF NOT EXISTS `url_cache` (
  `url_hash` VARCHAR(64) PRIMARY KEY,
  `url` TEXT NOT NULL,

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