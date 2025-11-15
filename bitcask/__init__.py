"""Bitcask implementation in Python"""

from .database import Bitcask
from .record import Record
from .file_manager import FileManager
from .index import HashTableIndex

__version__ = "1.0.0"
__author__ = "Manthan"
__description__ = "A simple log-structured Bitcask key-value store implementation in Python"

__all__ = ["Bitcask", "Record", "FileManager", "HashTableIndex", "IndexRecord"]