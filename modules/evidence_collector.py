import os
import subprocess
import zipfile
from datetime import datetime
import shutil
import socket

def collect_evidence(log):
    log("[*] Coletando evidências...")
    root = r"C:\Evidencias"
    os.makedirs(root, exist_ok=True)

    host = socket.gethostname()
    t = datetime.now().strftime("%Y%m%d-%H%M")
    base = os.path.join(root, f"{host}-{t}")
    os.makedirs(base, exist_ok=True)

    def run(cmd, out):
        r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        with open(os.path.join(base, out), "w", encoding="utf-8") as f:
            f.write(r.stdout)

    try:
        ip = socket.gethostbyname(host)
        with open(os.path.join(base, "system_info.txt"), "w", encoding="utf-8") as f:
            f.write(f"Hostname: {host}\nIP: {ip}\n")

        run("tasklist", "processes.txt")
        run("wmic startup get caption,command", "startup_programs.txt")
        run("netstat -ano", "network_connections.txt")
        run('powershell "Get-EventLog -LogName Application -Newest 200"', "eventlog_application.txt")
        run('powershell "Get-EventLog -LogName System -Newest 200"', "eventlog_system.txt")

        for f in [os.path.expanduser("~/Downloads"), os.path.expanduser("~/Desktop")]:
            if os.path.exists(f):
                try: shutil.copytree(f, os.path.join(base, os.path.basename(f)), dirs_exist_ok=True)
                except Exception as e: log(f"[!] Falha ao copiar {f}: {e}")

        log("[*] Compactando evidências...")
        zip_name = os.path.join(base, f"evidence_{t}.zip")
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
            for r, _, fs in os.walk(base):
                for file in fs:
                    p = os.path.join(r, file)
                    z.write(p, os.path.relpath(p, base))

        log(f"[+] Coleta concluída em {base}")
        subprocess.run(f'explorer "{base}"', shell=True)
    except Exception as e:
        log(f"[ERRO] {e}")
