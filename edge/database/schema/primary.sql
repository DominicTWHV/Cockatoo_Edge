CREATE TABLE IF NOT EXISTS `configs` (
    `security_repository` VARCHAR, -- github repository for security dataset, ex: DominicTWHV/CTI-DB-DUMP

    `auto_update` INT DEFAULT 1, -- whether to auto update the security dataset or not (1 = true, 0 = false)
    `update_interval` INT DEFAULT 0, -- interval to pull in dataset updates in minutes. Use 0 to set the time automatically

    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE IF NOT EXISTS `datasets` (
    `security_repository` VARCHAR PRIMARY KEY, -- github repository for security dataset, ex: DominicTWHV/CTI-DB-DUMP

    `in_use` INT DEFAULT 0, -- whether this dataset is actively being used (1 = true, 0 = false)
    `locked` INT DEFAULT 0, -- whether this dataset is locked from deletion (manually)

    `remote_update_interval` INT DEFAULT 0, -- how often in minutes is this dataset updates by the remote peer (set automatically, do not manually edit)
    
    `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)
