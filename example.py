import bitcask
from loguru import logger

def main():
    logger.info("Bitcask module imported successfully")

    db = bitcask.Bitcask("/tmp/tcask")
    db.put(b"key1", b"value1")
    logger.info(f"Current keys in the database: {db.keys()}")
    value = db.get(b"key1")
    logger.info(f"Retrieved value: {value}")
    db.delete(b"key1")
    logger.info(f"Current keys in the database: {db.keys()}")

    db.close()

    logger.info("Bitcask operations completed")


if __name__ == "__main__":
    main()
