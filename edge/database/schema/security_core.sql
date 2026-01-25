CREATE TABLE IF NOT EXISTS `url_cache` (
  `url_hash` VARCHAR(64) PRIMARY KEY,
  `url` TEXT NOT NULL,

  `times_seen` INT DEFAULT 1, -- how many times this url has been seen by core
  `scan_result` VARCHAR,
  `categorization` TEXT, -- Malicious, Suspicious, Harmless

  `is_redirect` INT, -- will be true if this url redirects elsewhere
  `downstream_target` VARCHAR DEFAULT 'N/A', -- the url that this url redirects to (final), if it does not redirect, this will be N/A
  -- note, if multiple hops, the final destination will be stored here, Intermediate hops will not be stored.

  `parent_set_name` VARCHAR, -- the dataset this url originated from

  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);

CREATE TABLE IF NOT EXISTS `file_hash_cache` (
  `sha256` VARCHAR PRIMARY KEY,
  `times_seen` INT DEFAULT 1, -- how many times this file has been seen
  `scan_result` VARCHAR,
  `categorization` VARCHAR, -- Malicious, Suspicious, Harmless

  `parent_set_name` VARCHAR, -- file type / extension

  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);

CREATE TABLE IF NOT EXISTS `invite_cache` (
  `invite` VARCHAR PRIMARY KEY, -- will be an argon2id hash
  `times_seen` INT DEFAULT 1, -- how many times this invite has been seen
  `categorization` VARCHAR, -- malicious, harmless, no need for a suspicious class here
  `resolution` VARCHAR, -- destination server name (may be partially obfuscated)

  `parent_set_name` VARCHAR, -- the dataset this url originated from

  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- auto timestamp for last seen time
);