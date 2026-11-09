# Тема: GIL basics → `sys.getswitchinterval`
# Запуск из папки lecture: python3 1_threading/24_switch_interval.py

import sys

print(f"switch interval = {sys.getswitchinterval() * 1000:.1f} ms")
