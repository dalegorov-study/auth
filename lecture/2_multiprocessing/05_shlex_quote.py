# Тема: `subprocess` — с чего начнём → `shell=True` — почему опасно
# Запуск из папки lecture: python3 2_multiprocessing/05_shlex_quote.py

import shlex

user_input = "nonexistent.txt; rm /tmp/secret.txt"
safe = shlex.quote(user_input)
print(f"escaped: {safe}")
print(f"full command: cat /tmp/{safe}")
