import subprocess
import time

def fix_printers(log):
    path = r"\\srv-wdsprint"
    try:
        log("[*] Reiniciando spooler...")
        subprocess.run("net stop spooler", shell=True)
        time.sleep(2)

        log("[*] Removendo impressoras...")
        subprocess.run('powershell "Get-Printer | Remove-Printer -Confirm:$false"', shell=True)

        log("[*] Removendo drivers...")
        subprocess.run('powershell "Get-PrinterDriver | Remove-PrinterDriver -Confirm:$false"', shell=True)

        time.sleep(2)
        log("[*] Iniciando spooler...")
        subprocess.run("net start spooler", shell=True)
        time.sleep(3)

        log(f"[*] Adicionando {path}")
        subprocess.run(f'rundll32 printui.dll,PrintUIEntry /in /n "{path}"', shell=True)

        log("[+] Impressoras resetadas.")
    except Exception as e:
        log(f"[ERRO] {e}")
