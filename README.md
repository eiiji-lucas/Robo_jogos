# Robo de Jogos para Telegram

Este projeto cria um bot Telegram que envia a lista de jogos do dia em esportes como futebol, basquete e Valorant, com horário cronológico, liga principal e canais de transmissão.

## Como usar

1. Crie um bot no Telegram com o BotFather e copie o token.
2. Copie `.env.example` para `.env` e preencha `TELEGRAM_TOKEN`.
3. (Opcional) Deixe `THE_SPORTS_DB_API_KEY=1` ou use sua chave própria.
4. Instale dependências:

```powershell
python -m pip install -r requirements.txt
```

5. Execute:

```powershell
& .\.venv\Scripts\Activate.ps1
python bot.py
```

6. No Telegram, envie `/start` e depois `/jogos` ou `/hoje`.

## Comandos

- `/start` — apresenta o bot.
- `/jogos` — lista os jogos do dia em ordem cronológica.
- `/hoje` — mesmo que `/jogos`.

## Como funciona

O bot consulta a API do TheSportsDB para eventos do dia e filtra ligas principais de futebol, basquete e Valorant.

Para adicionar WhatsApp, use a API da Meta ou Twilio e reaproveite a lógica de busca dos jogos.
