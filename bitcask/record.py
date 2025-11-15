"""Bitcask Record Module"""

import time
import struct
from typing import Optional, Tuple


class Record:
    """Represents a key-value record in Bitcask."""

    def __init__(self, key: str, value: Optional[bytes], is_tombstone: bool = False):
        self.key = key
        self.value = value
        self.timestamp = int(time.time())
        self.is_tombstone = is_tombstone

    def serialize(self) -> bytes:
        """
        Serializes the record to bytes for writing to log file
        Format: timestamp (4 bytes) | key_size (4 bytes) | value_size (4 bytes) | is_tombstone (1 byte) | key | value
        """

        key_bytes = self.key.encode('utf-8')
        key_size = len(key_bytes)

        if self.is_tombstone:
            value_bytes = b''
        else:
            value_bytes = self.value or b''

        value_size = len(value_bytes)
        header = struct.pack('>LLL?', self.timestamp, key_size, value_size, self.is_tombstone)
        return header + key_bytes + value_bytes

    @classmethod
    def deserialize(cls, data: bytes, offset: int = 0) -> Tuple[Optional['Record'], int]:
        """Deserializes bytes to a record + new offset"""

        header_size = 13 # 4 + 4 + 4 + 1

        if len(data) < offset + header_size:
            raise ValueError("Incomplete record header")

        # Unpack the header
        timestamp, key_size, value_size, is_tombstone = struct.unpack('>LLL?', data[offset:offset + header_size])
        offset += header_size

        # Read key
        key = data[offset:offset + key_size].decode('utf-8')
        offset += key_size

        # Read value
        if is_tombstone:
            value = None
        else:
            value = data[offset:offset + value_size]
        offset += value_size

        record = cls(key, value, is_tombstone)
        record.timestamp = timestamp
        return record, offset
    
    def __repr__(self):
        return f"Record(key={self.key!r}, value={self.value!r}, is_tombstone={self.is_tombstone}, timestamp={self.timestamp})"