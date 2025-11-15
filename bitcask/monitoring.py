import psutil

def get_cpu_usage():
    """Get the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Get the current memory usage statistics."""
    memory_info = psutil.virtual_memory()
    return {
        "total": memory_info.total,
        "used": memory_info.used,
        "percent": memory_info.percent
    }

