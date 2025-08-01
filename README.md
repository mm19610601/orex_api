# OREX API

API para receber localizações e autenticar utilizadores.

## Variáveis de ambiente necessárias

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD

## Endpoints

- POST /login
    - Body JSON: { "username": "...", "password": "..." }
    - Retorna: { "user_id": ... }

- POST /location
    - Body JSON: { "user_id": ..., "latitude": ..., "longitude": ..., "precisao": ..., "timestamp": "ISO8601" }
    - Regista localização do utilizador.

- GET /
    - Mensagem de status.

