import subprocess
import psutil

def get_bitlocker_status():
    """
    Verifica se o BitLocker está ativo na unidade C:
    Retorna 'On', 'Off' ou 'N/A'.
    """
    try:
        result = subprocess.run(
            'manage-bde -status C:',
            capture_output=True,
            text=True,
            shell=True
        )
        return "On" if "Percentual de criptografia" in result.stdout else "Off"
    except Exception:
        return "N/A"

def get_antivirus_status():
    """
    Verifica se o serviço 'Sophos Endpoint Defense Service' está em execução.
    Retorna 'On', 'Off' ou 'N/A'.
    """
    try:
        svc = psutil.win_service_get("Sophos Endpoint Defense Service")
        return "On" if svc.as_dict()["status"] == "running" else "Off"
    except Exception:
        return "N/A"
