## Installation
1. python3.11 -m venv venv
2. source venv/bin/activate
3. poetry install
4. docker compose up -d
5. скопировать env -> .env и заполнить секреты
6. заполнить files/initial_balances.json в формате {"<tg_id>" : {"<coin_name>": "<amount>"}} 
7. python -m src.main
