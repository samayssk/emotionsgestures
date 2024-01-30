import time
import psutil
import GPUtil
 
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)
 
def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent
 
def get_storage_usage():
    root_disk = psutil.disk_usage('/')
    return root_disk.percent
 
def get_gpu_usage():
    try:
        gpus = GPUtil.getGPUs()
        return [gpu.load * 100 for gpu in gpus]
    except Exception as e:
        return str(e)
 
def display_live_usage():
    while True:
        # CPU usage
        cpu_usage = get_cpu_usage()
        print(f'CPU Usage: {cpu_usage}%')
 
        # Memory (RAM) usage
        memory_usage = get_memory_usage()
        # print(f'Memory Usage: {memory_usage}%')
 
        # Storage usage
        storage_usage = get_storage_usage()
        # print(f'Storage Usage: {storage_usage}%')
        # print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)
        ram_info = psutil.virtual_memory()
        ram_percent = ram_info.percent
        print(f"RAM Usage: {ram_percent}%")
 
        # GPU usage (if available)
        try:
            gpu_usage = get_gpu_usage()
            print(f'GPU Usage: {gpu_usage}')
        except Exception as e:
            print(f'Error retrieving GPU usage: {e}')
 
        print('\n' + '=' * 40)  # Separator line
        time.sleep(0.5)  # Update every 1 second
 
if __name__ == "__main__":
    display_live_usage()