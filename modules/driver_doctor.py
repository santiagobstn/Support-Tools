import subprocess
import time

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
