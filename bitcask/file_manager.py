"""File Manager Module"""

import os
from typing import List, Dict, Tuple, Generator, Optional

from .record import Record


class FileManager:
    """
    Manages file operations for Bitcask
    """

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.log_file = None
        self.file_position = 0

    def open_log_file(self):
        """
        Opens a log file for appending and update file position
        """
        self.log_file = open(self.base_path, 'ab+')
        self.log_file.seek(0, os.SEEK_END)
        self.file_position = self.log_file.tell()

    def close_log_file(self):
        """
        Closes the log file
        """
        if self.log_file:
            self.log_file.close()
            self.log_file = None

    def write_record(self, record: Record) -> int:
        """
        Writes a record to the log file and return the position where it was written
        """
        if not self.log_file:
            raise ValueError("Log file is not open")

        # Write serialized record to file
        serialized_record = record.serialize()
        self.log_file.write(serialized_record)
        self.log_file.flush()

        # Update file position
        bytes_written = len(serialized_record)
        record_position = self.file_position
        self.file_position += bytes_written
    
        return record_position

    def read_record(self, offset: int, chunk_size: int = 1024) -> Record:
        """
        Reads a record from the log file at the given offset
        """
        with open(self.base_path, 'rb') as f:
            f.seek(offset)
            data = f.read(chunk_size)   
            if not data:
                raise ValueError("No data found at the given offset")
            record, _ = Record.deserialize(data, 0)
            return record

    def load_records(self) -> Generator[Tuple[Record, int], None, None]:
        """
        Loads all records from the log file
        """
        if not os.path.exists(self.base_path):
            return

        with open(self.base_path, 'rb') as f:
            data = f.read()
            offset = 0

            while offset < len(data):
                try:
                    record, new_offset = Record.deserialize(data, offset)
                    yield record, offset
                    offset = new_offset
                except ValueError:
                    break

        # update file position to last valid offset
        self.file_position = offset

    def compact_records(self, valid_records: Dict[str, bytes]) -> Dict[str, Tuple[int, int]]:
        """
        Compacts the log file by rewriting only valid records
        Returns a mapping of keys to their new positions and sizes
        """
        # Create a temporary file for compaction
        temp_file_path = self.base_path + ".tmp"
        new_hash_table = {}
        new_offset = 0

        # Write valid records to a temporary file
        with open(temp_file_path, 'wb') as temp_file:
            for key, value in valid_records.items():
                record = Record(key, value)
                serialized_record = record.serialize()
                temp_file.write(serialized_record)
                
                value_size = len(value)
                new_hash_table[key] = (new_offset, value_size)
                new_offset += len(serialized_record)

        self.close_log_file()

        # Replace old log file with compacted file
        os.replace(temp_file_path, self.base_path)
        self.open_log_file()
        return new_hash_table 

    def file_exists(self) -> bool:
        """Checks if the log file exists"""
        return os.path.exists(self.base_path)

    def get_file_size(self) -> int:
        """Returns the size of the log file"""
        if self.file_exists():
            return os.path.getsize(self.base_path)
        return 0

    def __enter__(self):
        self.open_log_file()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_log_file()