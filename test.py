# Get CPU usage
import psutil
from loguru import logger

cpu_percent = psutil.cpu_percent(interval=1)
logger.info(f"CPU Usage: {cpu_percent}%")


# Get memory usage
memory_info = psutil.virtual_memory()
logger.info(f"Total Memory: {memory_info.total / (1024**3):.2f} GB")
logger.info(f"Used Memory: {memory_info.used / (1024**3):.2f} GB")
logger.info(f"Memory Usage Percentage: {memory_info.percent}%")