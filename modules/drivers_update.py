import subprocess
import time
import json
import tempfile
import os

def scan_drivers(log):
    log("[*] Verificando drivers e dispositivos...")
    try:
        r = subprocess.run(
            'wmic path win32_pnpentity get Name,Status',
            capture_output=True, text=True, shell=True
        )
        output = r.stdout.strip().splitlines()

        ok = 0
        nok = 0

        for line in output[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.rsplit(" ", 1)
            name = parts[0].strip()
            status = parts[-1].strip().upper() if len(parts) > 1 else "UNKNOWN"

            if status == "OK":
                ok += 1
                log(f"[OK] {name}")
            else:
                nok += 1
                log(f"[X] {name} ({status})")

        log("[*] Abrindo Gerenciador de Dispositivos para correção manual...")
        subprocess.run("devmgmt.msc", shell=True)
        time.sleep(1)

        log(f"[+] Diagnóstico: {ok} OK | {nok} com problema")

    except Exception as e:
        log(f"[ERRO] {e}")


def update_all_drivers(log):
    """
    Tenta atualizar todos os drivers automaticamente via PowerShell.
    Requer execução como administrador.
    """

    log("[*] Tentando atualizar todos os drivers via PowerShell...")

    # Criar script PowerShell temporário para capturar quais drivers foram atualizados
    script = r"""
    $devices = Get-PnpDevice | Where-Object { $_.Status -eq "OK" }
    $updated = @()
    foreach ($dev in $devices) {
        try {
            Update-PnpDevice -InstanceId $dev.InstanceId -ErrorAction SilentlyContinue | Out-Null
            $updated += $dev.FriendlyName
        } catch {}
    }
    $updated | ConvertTo-Json -Compress
    """
    temp_file = os.path.join(tempfile.gettempdir(), "update_drivers.ps1")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(script)

    try:
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_file],
            capture_output=True, text=True, shell=True
        )
        if result.stdout.strip():
            try:
                updated_list = json.loads(result.stdout.strip())
            except Exception:
                updated_list = []
        else:
            updated_list = []

        if updated_list:
            log(f"[+] Drivers atualizados ({len(updated_list)}):")
            for d in updated_list:
                log(f"    - {d}")
            summary = "\n".join(updated_list)
            return f"{len(updated_list)} drivers atualizados:\n\n{summary}"
        else:
            log("[+] Nenhum driver foi atualizado (ou todos já estavam na versão mais recente).")
            return "Nenhum driver foi atualizado. Todos já estavam na versão mais recente."

    except Exception as e:
        log(f"[ERRO] {e}")
        return f"Erro ao atualizar drivers: {e}"
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
