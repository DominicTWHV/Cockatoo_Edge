CREATE TABLE IF NOT EXISTS `configs` (
    `server_id` VARCHAR PRIMARY KEY, -- server identifier

    `mal_url_action` INT DEFAULT 0, -- action to take on malicious URL detection (0 = log, 1 = warn, 2 = delete and warn)
    `mal_file_action` INT DEFAULT 0, -- action to take on malicious file detection (0 = log, 1 = warn, 2 = delete and warn)
    `mal_invite_action` INT DEFAULT 0, -- action to take on malicious invite detection (0 = log, 1 = warn, 2 = delete and warn)

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `moderation_logs` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,

    `server_id` VARCHAR, -- server identifier
    `user_id` VARCHAR, -- user identifier
    `triggered_by` VARCHAR, -- url/file/invite that triggered the action
    `action_taken` VARCHAR, -- action taken (log/warn/delete)

    `malicious_entry` VARCHAR, -- the malicious url/file/invite detected
    `source_dataset` VARCHAR, -- dataset from which the malicious entry originated

    `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP -- time of the action
);