# Тема: Subinterpreters — PEP 684 → Обмен данными между интерпретаторами
# Запуск из папки lecture: python3 2_multiprocessing/17_subinterpreter_queue.py
# Нужен Python 3.14+

from concurrent import interpreters

q = interpreters.create_queue()
interp = interpreters.create()

# Передаём queue в subinterp — работает
interp.prepare_main(q=q)
interp.exec("q.put('hello from subinterp')")

msg = q.get()
print(f"main got: {msg}")

interp.close()
