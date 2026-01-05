CREATE TABLE IF NOT EXISTS `configs` (
    `security_repository_url` VARCHAR, -- github repository for url security dataset, ex: DominicTWHV/CTI-DB-DUMP
    `security_repository_file` VARCHAR, -- github file path for file security dataset
    `security_repository_invite` VARCHAR, -- github file path for invite security dataset (all three can be the same if supported)

    `auto_update` INT DEFAULT 1, -- whether to auto update the security dataset or not (1 = true, 0 = false)
    `update_interval` INT DEFAULT 0, -- interval to pull in dataset updates in minutes. Use 0 to set the time automatically

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `actions` (
    `server_id` VARCHAR PRIMARY KEY, -- server identifier

    `mal_url_action` INT DEFAULT 0, -- action to take on malicious URL detection (0 = log, 1 = warn, 2 = delete and warn)
    `mal_file_action` INT DEFAULT 0, -- action to take on malicious file detection (0 = log, 1 = warn, 2 = delete and warn)
    `mal_invite_action` INT DEFAULT 0, -- action to take on malicious invite detection (0 = log, 1 = warn, 2 = delete and warn)

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)
