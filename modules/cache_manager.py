import os
import shutil
import subprocess

def cleanup_cache(log):
    log("[*] Limpando arquivos temporários e cache...")

    before = shutil.disk_usage("C:\\").free

    def limpar(path):
        if os.path.exists(path) and os.path.isdir(path):
            try:
                shutil.rmtree(path, ignore_errors=True)
                log(f"[OK] Limpo: {path}")
            except Exception as e:
                log(f"[!] Erro ao limpar {path}: {e}")

    # Pastas básicas
    temp = os.environ.get("TEMP", "")
    limpar(temp)

    limpar(r"C:\Windows\Prefetch")

    # Teams
    teams = os.path.expanduser(r"~\\AppData\\Roaming\\Microsoft\\Teams")
    for sub in ["application cache","blob_storage","Cache","databases","GPUCache","IndexedDB","Local Storage","tmp"]:
        limpar(os.path.join(teams, sub))

    # Outlook e Office
    limpar(os.path.expanduser(r"~\\AppData\\Local\\Microsoft\\Outlook"))
    limpar(os.path.expanduser(r"~\\AppData\\Local\\Microsoft\\Office\\16.0\\OfficeFileCache"))

    # Navegadores
    limpar(os.path.expanduser(r"~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache"))
    limpar(os.path.expanduser(r"~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache"))

    # Firefox
    ff = os.path.expanduser(r"~\\AppData\\Local\\Mozilla\\Firefox\\Profiles")
    if os.path.exists(ff):
        for p in os.listdir(ff):
            limpar(os.path.join(ff, p, "cache2"))

    # Resetar cache da Microsoft Store
    subprocess.run("wsreset.exe", shell=True)

    after = shutil.disk_usage("C:\\").free
    freed = max(0, (after - before) / (1024 * 1024))
    log(f"[+] Limpeza concluída. Espaço liberado: {freed:.2f} MB")
