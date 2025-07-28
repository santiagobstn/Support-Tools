# Support Tools – Made by: Santiago

Ferramenta interna para suporte em Windows com interface gráfica (Python + PyQt5).
Facilita o trabalho de TI automatizando diagnósticos e tarefas comuns.

---

## Funcionalidades

### 1. Machine Infos
- Mostra todas as informações da máquina usando `systeminfo`.

### 2. Cache & Temp Manager
- Limpa:
  - `%TEMP%`
  - Cache do Windows (Prefetch)
  - Cache do Teams
  - Cache do Outlook/Office
  - Cache de navegadores (Edge, Chrome, Firefox)
- Faz `wsreset` para limpar cache da Microsoft Store.

### 3. Printer Fixer
- Remove todas as impressoras e drivers
- Reinicia o serviço de spooler
- Reinstala a impressora padrão `\\srv-wdsprint`

### 4. Driver Doctor
- Lista drivers e dispositivos
- Destaca os que têm problemas
- Abre automaticamente o Gerenciador de Dispositivos
- Exibe um diagnóstico final

### 5. Evidence Collector
- Coleta:
  - Processos ativos
  - Logs do Windows (eventos recentes)
  - Conexões de rede
  - Programas na inicialização
  - Desktop e Downloads do usuário
- Compacta tudo em `C:\Evidencias\{PC}-{Data}`
- Abre a pasta ao finalizar

### 6. See Evidences
- Abre diretamente a pasta `C:\Evidencias`

---

## Como executar

### 1. Executar direto no Python

Requisitos:
- Python 3.9 ou superior
- Dependências:

pip install PyQt5

Executar:

python main.py

---

### 2. Gerar um executável (.exe)

Já existe um script `build.bat` na raiz do projeto.
Ele:

* Limpa pastas antigas (`build`, `dist`)
* Gera o `.exe` com ícone
* Renomeia para `Support_Tools.exe`
* Abre a pasta `dist` no final

Para usar:

* Clique duas vezes em `build.bat`
* O executável final estará em `dist\Support_Tools.exe`

Ou rode manualmente:

pyinstaller --onefile --noconsole --icon=icons\icon.ico main.py

---

## Estrutura do projeto

Support Tools/
│
├── modules/
│   ├── cache_manager.py
│   ├── driver_doctor.py
│   ├── evidence_collector.py
│   ├── printer_fixer.py
│
├── icons/
│   └── icon.ico
│
├── build.bat
├── main.py
├── README.md
└── .gitignore

---

## Tecnologias

* Python 3
* PyQt5
* PowerShell e utilitários do Windows

---

## Autor

Santiago
