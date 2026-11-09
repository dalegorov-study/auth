# Тема: `subprocess` — с чего начнём → `shell=True` — почему опасно
# Запуск из папки lecture: python3 2_multiprocessing/04_injection_safe.py

import subprocess
from pathlib import Path

Path("/tmp/secret.txt").write_text("важные данные\n")

user_input = "nonexistent.txt; rm /tmp/secret.txt"

print("=== ХОРОШО (список аргументов) ===")
result = subprocess.run(
    ["cat", f"/tmp/{user_input}"],
    capture_output=True,
    text=True,
    check=False,
)
print(f"stderr: {result.stderr.strip()}")
print(f"secret.txt exists? {Path('/tmp/secret.txt').exists()}")
