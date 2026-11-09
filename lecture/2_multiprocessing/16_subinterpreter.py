# Тема: Subinterpreters — PEP 684
# Запуск из папки lecture: python3 2_multiprocessing/16_subinterpreter.py
# Нужен Python 3.14+

from concurrent import interpreters

interp = interpreters.create()
print(f"created: {interp}")

# Выполняем код в subinterpreter'е
interp.exec(
    "import os\n"
    "print('in subinterp: pid=', os.getpid(), 'name=', __name__)\n"
    "x = 42\n"
)

# Каждый subinterpreter — свой namespace, но тот же процесс (тот же pid).
# Между интерпретаторами память не разделяется (в текущей реализации).

interp.close()
print("subinterpreter closed")
