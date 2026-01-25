class SetDownload:

    removed_files = ["metadata.json", "domains.json"]

class GithubMetaStore:
    entry_names = [
        "licensing",
        "dataset_type",
        "remote_update_interval",
        "num_of_url_entries",
        "num_of_file_entries",
        "num_of_invite_entries"
    ]

class GenericMetaStore:
    entry_names = [
        "licensing",
        "dataset_type"
    ]