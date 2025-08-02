import psutil
import platform
import socket
import datetime
import os

def get_machine_info():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    return {
        "Host": socket.gethostname(),
        "IP": socket.gethostbyname(socket.gethostname()),
        "OS": f"{platform.system()} {platform.release()}",
        "CPU": f"{psutil.cpu_percent()}%",
        "RAM": f"{psutil.virtual_memory().percent}%",
        "Uptime": str(uptime).split('.')[0],
        "User": os.getlogin(),
    }
