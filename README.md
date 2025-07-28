# Support Tools

Ferramenta interna para suporte em Windows com interface gráfica:

## Funcionalidades

### 1. AutoFix / Limpeza
- Limpa caches do Windows, Teams e Outlook/Office
- Limpa `%TEMP%`
- Reinicia o Explorer para liberar memória

### 2. Resetar Impressoras
- Remove todas as impressoras e drivers
- Reinicia o spooler de impressão
- Reinstala a impressora padrão (`\\srv-wdsprint`)

## Como executar

### Diretamente (Python)
```bash
python support_tools.py
