# Тема: `subprocess` — с чего начнём → Практический пример: вызов git
# Запуск из папки lecture: python3 2_multiprocessing/06_git_version.py

import subprocess

result = subprocess.run(
    ["git", "--version"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.stdout.strip())
