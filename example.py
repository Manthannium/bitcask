from bitcask import Bitcask

with Bitcask("my.db") as db:
    db.put("name", b"Alice")
    print(db.get("name"))  # Output: b'Alice'
    print(db.keys())    # Output: ['name']

    db.delete("name")
    print(db.get("name"))  # Output: None
    print(db.keys())    # Output: []
    
    db.put("age", b"30")
    print(db.get("age"))  # Output: b'30'
    print(db.size())  # Output: 1
    db.compact()
    print(db.size())  # Output: 1

