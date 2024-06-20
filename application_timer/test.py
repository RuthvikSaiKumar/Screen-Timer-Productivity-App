import psutil

# Get a list of all running process
for proc in psutil.process_iter(['pid', 'name']):
    try:
        info = proc.info
        print(f"Process ID: {info['pid']} - Process Name: {info['name']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass