# Тема: `subprocess` — с чего начнём → `Popen` — контроль над процессом
# Запуск из папки lecture: python3 2_multiprocessing/02_popen_stream.py

import subprocess

proc = subprocess.Popen(
    ["python3", "-c", "import time; [print(i) for i in range(3)]; time.sleep(0.5)"],
    stdout=subprocess.PIPE,
    text=True,
)

# Читаем построчно как приходит
for line in proc.stdout:
    print(f"got: {line.strip()}")

proc.wait()
print(f"exit: {proc.returncode}")
