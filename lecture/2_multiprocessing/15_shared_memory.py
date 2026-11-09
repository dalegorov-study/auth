# Тема: IPC — как процессы обмениваются данными → `shared_memory` — zero-copy для bytes
# Запуск из папки lecture: python3 2_multiprocessing/15_shared_memory.py

from multiprocessing import shared_memory
import struct

# Producer: создать shared block и записать данные
shm = shared_memory.SharedMemory(create=True, size=1024)
shm.buf[:4] = struct.pack("i", 42)  # int в первые 4 байта
shm.buf[4:8] = struct.pack("i", 100)

print(f"created shm name: {shm.name}")
print(f"read from same block: {struct.unpack('i', shm.buf[:4])[0]}, {struct.unpack('i', shm.buf[4:8])[0]}")

# В другом процессе можно было бы:
# other = shared_memory.SharedMemory(name=shm.name)  # zero-copy attach
# data = struct.unpack('i', other.buf[:4])[0]

shm.close()
shm.unlink()  # удалить блок из системы
