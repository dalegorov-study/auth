# Тема: `subprocess` — с чего начнём → `subprocess.run` — простой случай
# Запуск из папки lecture: python3 2_multiprocessing/01_subprocess_run.py

import subprocess

result = subprocess.run(
    ["python3", "-c", "print('hello from subprocess')"],
    capture_output=True,
    text=True,
    check=True,
    timeout=5,
)
print(f"stdout: {result.stdout.strip()}")
print(f"return code: {result.returncode}")
