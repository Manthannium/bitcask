"""Bitcask database main module"""

from typing import Optional, List

from .file_manager import FileManager
from .index import HashTableIndex
from .record import Record

class Bitcask:
    """Main class for the Bitcask database"""

    def __init__(self, db_path: str = "bitcask.db"):
        self.db_path = db_path
        self.file_manager = FileManager(db_path)
        self.index = HashTableIndex()
        self.intialize()

    def intialize(self):
        """Initializes the database by loading existing records into the index"""

        self.file_manager.open_log_file()
        self.load_index_from_log()

    def load_index_from_log(self):
        """Loads the index from the log file"""

        for record, offset in self.file_manager.load_records():
            if record.is_tombstone:
                self.index.delete(record.key)
            else:
                self.index.put(record.key, offset, len(record.value))

    def put(self, key: str, value: bytes):
        """Stores a key-value pair in the database"""

        record = Record(key, value)
        offset = self.file_manager.write_record(record)
        value_size = len(value)
        self.index.put(key, offset, value_size)

    def get(self, key: str) -> Optional[bytes]:
        """Retrieves a value by key from the database"""
        index_record = self.index.get(key)

        if not index_record:
            return None

        try:
            record = self.file_manager.read_record(index_record.offset)
            return record.value
        except Exception:
            self.index.delete(key)
            return None

    def delete(self, key: str) -> bool:
        """Deletes a key-value pair from the database"""
        tombstone_record = Record(key, None, is_tombstone=True)
        self.file_manager.write_record(tombstone_record)
        self.index.delete(key)

    def keys(self) -> List[str]:
        """Returns a list of all keys in the database"""
        return self.index.keys()

    def size(self) -> int:
        """Returns the number of key-value pairs in the database"""
        return self.index.size()

    def contains(self, key: str) -> bool:
        """Checks if the database contains the given key"""
        return self.index.contains(key)

    def compact(self):
        """Compacts the database by rewriting it without deleted records"""
        if self.size() == 0:
            return

        # collect current valid records
        valid_records = {}
        for key in self.index.keys():
            value = self.get(key)
            if value is not None:
                valid_records[key] = value

        new_hash_table = self.file_manager.compact_records(valid_records)
        self.index.update_from_legacy_format(new_hash_table)

    def get_stats(self) -> dict:
        """Returns statistics about the database"""
        return {
            "num_keys": self.size(),
            "log_file_size": self.file_manager.get_file_size(),
        }

    def close(self):
        """Closes the database and its resources"""
        self.file_manager.close_log_file()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __len__(self):
        return self.size()

    def __contains__(self, key: str) -> bool:
        return self.index.contains(key)

    def __repr__(self):
        return f"BitcaskDatabase(path={self.db_path!r}, num_keys={self.size()})"
