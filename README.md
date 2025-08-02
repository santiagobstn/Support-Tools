# Support Tools

Uma ferramenta interna para suporte e automação de tarefas no Windows, desenvolvida para auxiliar na manutenção, diagnóstico e otimização de máquinas.

## Funcionalidades

### 1. Cache Temp Manager
- Limpeza automática de:
  - Pastas temporárias (%TEMP%)
  - Cache do Windows (Prefetch)
  - Cache do Teams
  - Cache do Outlook/Office
  - Cache de navegadores (Edge, Chrome, Firefox)
- Executa wsreset.exe para limpar cache da Microsoft Store.
- Mostra relatório do espaço liberado ao final.

### 2. Printer Fixer
- Reinicia o serviço de spooler.
- Remove todas as impressoras e drivers instalados.
- Reinstala automaticamente a impressora padrão da rede.
- Observação: requer executar o programa como administrador.

### 3. Evidence Collector
- Coleta evidências e gera relatórios (logs) em C:\Evidencias.

### 4. Drivers Update
- Atualiza automaticamente todos os drivers do sistema.
- Exibe um resumo dos drivers atualizados ao final.

## Interface

### Tela Principal
- Logo centralizada no topo.
- Informações da máquina:
  - Hostname, usuário, sistema operacional
  - Disco usado/total
  - Uso de RAM e CPU
  - Status do BitLocker e antivírus
  - Tempo de uptime
- Botões principais organizados em uma grade limpa e uniforme.
- Links no rodapé:
  - See Evidences – abre a pasta C:\Evidencias
  - View Logs – exibe as últimas ações executadas.

## Pré-requisitos

- Windows 10/11
- Python 3.10+ com:
  pip install pyqt5 psutil
- Executar como administrador para:
  - Atualizar drivers
  - Corrigir impressoras
  - Coletar algumas evidências do sistema

## Como executar

### Via Python:
python main.py

### Via Executável:
Gere um .exe com:
pyinstaller --onefile --noconsole --icon=icons/icon.ico main.py

Ou use o build.bat incluído no projeto.

## Estrutura do Projeto
Support-Tools/
├── main.py
├── app.manifest
├── build.bat
├── icons/
│   ├── icon.ico
│   └── icon.png
├── modules/
│   ├── cache_manager.py
│   ├── drivers_update.py
│   ├── evidence_collector.py
│   ├── printer_fixer.py
│   ├── machine_status.py
│   └── security_status.py
└── README.md

## Notas
- Desenvolvido por Santiago para uso interno.
