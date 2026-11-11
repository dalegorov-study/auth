# Тема: `subprocess` — с чего начнём → `shell=True` — почему опасно
# Запуск из папки lecture: python3 2_multiprocessing/03_injection_demo.py

import subprocess
from pathlib import Path

# готовим "цель" атаки - файл, который "не должен" исчезнуть
Path("/tmp/secret.txt").write_text("важные данные\n")
assert Path("/tmp/secret.txt").exists()

user_input = "nonexistent.txt; rm /tmp/secret.txt"

print("=== ПЛОХО (shell=True) ===")
subprocess.run(
    f"cat /tmp/{user_input}",
    shell=True,
    capture_output=True,
    check=False,
)
print(f"secret.txt exists? {Path('/tmp/secret.txt').exists()}")
