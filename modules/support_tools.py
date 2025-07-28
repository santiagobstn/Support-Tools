import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import shutil
from datetime import datetime
import time

# -------------------------
# CONFIG
# -------------------------
output_root = r"C:\Evidencias\AutoFix"
printer_path = r"\\srv-wdsprint"
os.makedirs(output_root, exist_ok=True)

# -------------------------
# FUNÇÕES
# -------------------------

def log(msg, log_file):
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def limpar_cache():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    log_file = os.path.join(output_root, f"AutoFix_{timestamp}.txt")
    messagebox.showinfo("AutoFix", "Iniciando limpeza, pode demorar alguns minutos...")

    def try_delete(path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
                log(f"[OK] Limpo: {path}", log_file)
        except Exception as e:
            log(f"[ERRO] {path} -> {e}", log_file)

    log("[*] Limpando arquivos temporários...", log_file)
    temp_path = os.environ.get("TEMP", "")
    try_delete(temp_path)

    log("[*] Limpando cache do Teams...", log_file)
    teams_cache = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Teams")
    for sub in ["application cache", "blob_storage", "Cache", "databases", "GPUCache", "IndexedDB", "Local Storage", "tmp"]:
        try_delete(os.path.join(teams_cache, sub))

    log("[*] Limpando cache do Office/Outlook...", log_file)
    office_cache = os.path.expanduser(r"~\AppData\Local\Microsoft\Office")
    try_delete(os.path.join(office_cache, "16.0\\OfficeFileCache"))
    try_delete(os.path.expanduser(r"~\AppData\Local\Microsoft\Outlook"))

    log("[*] Limpando cache da Windows Store...", log_file)
    subprocess.run("wsreset.exe", shell=True)

    log("[*] Reiniciando Explorer...", log_file)
    subprocess.run("taskkill /F /IM explorer.exe", shell=True)
    subprocess.run("start explorer.exe", shell=True)

    log("\n[+] AutoFix finalizado!", log_file)
    messagebox.showinfo("AutoFix", f"Limpeza concluída!\nLog salvo em:\n{log_file}")
    subprocess.run(f'explorer "{output_root}"', shell=True)

def resetar_impressoras():
    confirmar = messagebox.askyesno("Resetar Impressoras", "Isso vai remover TODAS as impressoras e reinstalar a padrão.\nDeseja continuar?")
    if not confirmar:
        return

    try:
        messagebox.showinfo("Impressoras", "Reinicializando serviços de spooler...")
        subprocess.run("net stop spooler", shell=True)
        time.sleep(2)

        subprocess.run('powershell "Get-Printer | Remove-Printer -Confirm:$false"', shell=True)
        subprocess.run('powershell "Get-PrinterDriver | Remove-PrinterDriver -Confirm:$false"', shell=True)

        time.sleep(2)
        subprocess.run("net start spooler", shell=True)
        time.sleep(3)

        subprocess.run(f'rundll32 printui.dll,PrintUIEntry /in /n "{printer_path}"', shell=True)

        messagebox.showinfo("Impressoras", "Reset concluído e impressora padrão adicionada!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# -------------------------
# INTERFACE TKINTER
# -------------------------

root = tk.Tk()
root.title("Ferramentas de Suporte - TI")
root.geometry("400x200")

lbl = tk.Label(root, text="Escolha a ação:", font=("Segoe UI", 14))
lbl.pack(pady=10)

btn1 = tk.Button(root, text="AutoFix / Limpeza", font=("Segoe UI", 12), command=limpar_cache, width=20, height=2)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Resetar Impressoras", font=("Segoe UI", 12), command=resetar_impressoras, width=20, height=2)
btn2.pack(pady=10)

root.mainloop()
