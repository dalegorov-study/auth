# Тема: `threading` — базовые примитивы → Что такое поток
# Запуск из папки lecture: python3 1_threading/02_cpu_topology.py

import subprocess

# Детали по железу: lscpu на Linux, sysctl на macOS
subprocess.run(
    'lscpu | grep -E "^(CPU\\(s\\)|Thread|Core|Socket)" 2>/dev/null || '
    'sysctl -n hw.physicalcpu hw.logicalcpu',
    shell=True,
)
