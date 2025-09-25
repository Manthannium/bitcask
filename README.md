# ⚡ Bitcask

> **A blazing-fast, log-structured key-value storage engine in Python** 🐍


## 📚 What is Bitcask?

Bitcask is a key-value storage engine originally developed by Basho for Riak. It’s designed for speed and simplicity, using a log-structured approach:

- **Append-Only Writes**: All updates are appended to disk, minimizing random writes.
- **In-Memory Index**: Keys are indexed in memory for fast lookups.
- **Compaction**: Old log segments are periodically merged to remove stale data.

Bitcask is ideal for workloads with high write throughput and where keys fit in memory.

---

## 🌟 Features

- ⚡ **High Performance**: Fast read/write operations using append-only log files.
- 🗝️ **Key-Value Store**: Simple API for storing and retrieving binary data by key.
- 🧩 **Concurrency**: Safe for concurrent access with file locks.
- 🗃️ **Efficient Storage**: Uses log-structured files for minimal disk seeks.
- 🧹 **Automatic Compaction**: Periodically merges log files to reclaim space.
- 🔒 **Crash Safety**: Durable writes with minimal risk of data loss.
- 📦 **Easy Integration**: Lightweight and simple to embed in Python projects.

---

## ⚠️ Limitations

- **Keys Must Fit in Memory**: The in-memory index requires all keys to be stored in RAM, limiting dataset size by available memory.
- **No Range Queries**: Bitcask only supports point lookups; scanning or range queries are not supported.
- **Large Values Not Optimized**: Storing very large values can impact performance due to log file structure.
- **Single Directory Storage**: All data files are stored in a single directory, which may not scale for extremely large datasets.
- **Compaction Overhead**: Periodic compaction can temporarily increase disk and CPU usage.
- **No Built-in Replication**: Bitcask does not provide replication or clustering out of the box.

---

## 🏗️ How It Works

1. **Write**: Data is appended to a log file. The in-memory index maps keys to file offsets.
2. **Read**: The index is used to locate the value on disk quickly.
3. **Delete**: A tombstone record is written to the log.
4. **Compaction**: Periodically, log files are merged to remove deleted/overwritten entries.

---

## Architecture
<Add here>

---

## Project Structure
```bitcask/
├── bitcask/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── bitcask.py
│   │   ├── data_file.py
│   │   ├── hint_file.py
│   │   ├── keydir.py
│   │   └── exceptions.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── crc.py
│   │   ├── serialization.py
│   │   └── file_utils.py
│   └── cli/
│       ├── __init__.py
│       ├── main.py
│       └── commands.py
├── tests/
│   ├── __init__.py
│   ├── test_bitcask.py
│   ├── test_data_file.py
│   ├── test_keydir.py
│   └── test_cli.py
├── docs/
│   ├── README.md
│   ├── api.md
│   └── examples/
│       ├── basic_usage.py
│       └── advanced_usage.py
├── scripts/
│   └── benchmark.py
├── setup.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
└── Makefile
```
---

## 🛠️ Usage

```python
from bitcask import Bitcask

db = Bitcask('/path/to/db')

# Set a value
db.put(b'mykey', b'myvalue')

# Get a value
value = db.get(b'mykey')

# Delete a key
db.delete(b'mykey')

# Close the database
db.close()
```

---

## 📈 Performance

- **Write throughput**: Extremely high due to append-only design.
- **Read latency**: Low, as keys are indexed in memory.
- **Space efficiency**: Compaction keeps disk usage low.

---

## 📝 Design Principles

- **Simplicity**: Minimal dependencies, easy to understand.
- **Durability**: Data is safe on disk after each write.
- **Speed**: Optimized for SSDs and modern disks.

---

## 📦 Installation

```sh
pip install bitcask
```

---

## 🧪 Testing

```sh
pytest tests/
```

---

## 📄 License

MIT © 2025 Manthan Patel

---

## 🙏 Acknowledgements

- Inspired by [Basho’s Bitcask](https://github.com/basho/bitcask)
- Thanks to the open-source community!

---

## 💬 Contributing

Pull requests and issues are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📚 References

- [Bitcask Paper (PDF)](https://riak.com/assets/bitcask-intro.pdf)
- [Basho Bitcask GitHub](https://github.com/basho/bitcask)
