"""Index management module for Bitcask"""

from typing import Dict, Optional, Tuple, List

class IndexRecord:
    """Represents a record in hash table index"""

    def __init__(self, offset: int, value_size: int):
        self.offset = offset
        self.value_size = value_size

    def __repr__(self):
        return f"IndexRecord(offset={self.offset}, value_size={self.value_size})"

class HashTableIndex:
    """In-memory hash table index for Bitcask"""

    def __init__(self):
        self.index: Dict[str, IndexRecord] = {}

    def put(self, key: str, offset: int, value_size: int):
        """Adds or updates an index record for the given key"""
        self.index[key] = IndexRecord(offset, value_size)

    def get(self, key: str) -> Optional[IndexRecord]:
        """Retrieves the index record for the given key"""
        return self.index.get(key)

    def delete(self, key: str) -> bool:
        """Deletes the index record for the given key"""
        if key in self.index:
            del self.index[key]
            return True
        return False

    def contains(self, key: str) -> bool:
        """Checks if the index contains the given key"""
        return key in self.index

    def keys(self) -> List[str]:
        """Returns a list of all keys in the index"""
        return list(self.index.keys())

    def size(self) -> int:
        """Returns the number of records in the index"""
        return len(self.index)

    def __len__(self):
        return self.size()

    def clear(self):
        """Clears the index"""
        self.index.clear()

    def __repr__(self):
        return f"HashTableIndex(size={len(self.index)})"

    def __iter__(self):
        return iter(self.index)

    def update_from_legacy_format(self, legacy_index: Dict[str, Tuple[int, int]]):
        """Updates the index from a legacy format mapping keys to (offset, value_size) tuples"""
        self.clear()
        for key, (offset, value_size) in legacy_index.items():
            self.put(key, offset, value_size)

    def to_legacy_format(self) -> Dict[str, Tuple[int, int]]:
        """Converts the index to a legacy format for compatibility"""
        return {key: (record.offset, record.value_size) for key, record in self.index.items()}

    