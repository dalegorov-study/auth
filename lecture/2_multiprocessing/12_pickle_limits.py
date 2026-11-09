# Тема: IPC — как процессы обмениваются данными → Ограничение: pickle-only
# Запуск из папки lecture: python3 2_multiprocessing/12_pickle_limits.py

import pickle

# ok — обычная функция на уровне модуля picklable
def module_level(x): return x * 2

# НЕ ok — closure
def factory(multiplier):
    def inner(x): return x * multiplier
    return inner

# НЕ ok — lambda
lam = lambda x: x + 1

# НЕ ok — локальный класс
def make_class():
    class Local: pass
    return Local()

try:
    pickle.dumps(factory(3))
except (pickle.PicklingError, AttributeError) as e:
    print(f"factory(3): {type(e).__name__}: {e}")

try:
    pickle.dumps(lam)
except (pickle.PicklingError, AttributeError) as e:
    print(f"lambda: {type(e).__name__}: {e}")

try:
    pickle.dumps(make_class())
except (pickle.PicklingError, AttributeError) as e:
    print(f"local class: {type(e).__name__}: {e}")

print(f"module-level ok: {pickle.dumps(module_level)[:20]!r}...")
