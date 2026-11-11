"""π через Monte Carlo — три подхода к параллелизму. См. README.md."""


def _hits_in_circle(n_points: int, seed: int) -> int:
    """helper: количество точек в единичном круге (top-level функция —
    чтобы pickle работал для Pool)."""
    ...


def estimate_pi_serial(n_points: int) -> float:
    ...


def estimate_pi_threading(n_points: int, workers: int = 4) -> float:
    ...


def estimate_pi_multiprocessing(n_points: int, workers: int = 4) -> float:
    ...
