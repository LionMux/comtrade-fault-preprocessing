"""
Классификация вида короткого замыкания (КЗ) по симметричным составляющим.

Используется для:
1. Выбора модели из ансамбля при инференсе
2. Разделения датасета по типам КЗ при обучении

Алгоритм:
    По отношениям I₂/I₁ и I₀/I₁ (действующие значения после КЗ)
    определяется тип КЗ:
    
    • 3ф:   I₂/I₁ < 0.15  и  I₀/I₁ < 0.15
    • 2ф:   I₂/I₁ > 0.7  и  I₀/I₁ < 0.25
    • 1ф-З: I₂/I₁ > 0.7  и  I₀/I₁ > 0.7
    • 2ф-З: 0.25 < I₂/I₁ < 0.7  и  0.25 < I₀/I₁ < 0.7
    • неопределено: всё остальное
"""

import numpy as np
from typing import Tuple


# Пороги классификации (можно вынести в config)
THRESHOLD_21_LOW = 0.15   # нижняя граница I₂/I₁
THRESHOLD_21_HIGH = 0.7   # верхняя граница I₂/I₁
THRESHOLD_01_LOW = 0.25   # нижняя граница I₀/I₁
THRESHOLD_01_HIGH = 0.7   # верхняя граница I₀/I₁

FAULT_TYPES = ['3ф', '2ф', '2ф-З', '1ф-З', 'неопределено']


def classify_fault_type(I1_rms: float, I2_rms: float, I0_rms: float) -> Tuple[str, np.ndarray, Tuple[float, float]]:
    """Классификация вида КЗ по действующим значениям симметричных составляющих.

    Parameters
    ----------
    I1_rms, I2_rms, I0_rms : float
        Действующие значения прямой, обратной и нулевой последовательностей тока.

    Returns
    -------
    fault_type : str
        Один из: '3ф', '2ф', '2ф-З', '1ф-З', 'неопределено'.
    one_hot : np.ndarray, shape (4,)
        One-hot кодировка для 4 основных типов (без 'неопределено').
    ratios : tuple(float, float)
        (I₂/I₁, I₀/I₁) — отношения для отладки.
    """
    ratio_21 = I2_rms / (I1_rms + 1e-10)
    ratio_01 = I0_rms / (I1_rms + 1e-10)

    if ratio_21 < THRESHOLD_21_LOW and ratio_01 < THRESHOLD_21_LOW:
        fault_type = '3ф'
        one_hot = np.array([1, 0, 0, 0], dtype=np.float32)
    elif ratio_21 > THRESHOLD_21_HIGH and ratio_01 < THRESHOLD_01_LOW:
        fault_type = '2ф'
        one_hot = np.array([0, 1, 0, 0], dtype=np.float32)
    elif ratio_21 > THRESHOLD_21_HIGH and ratio_01 > THRESHOLD_01_HIGH:
        fault_type = '1ф-З'
        one_hot = np.array([0, 0, 0, 1], dtype=np.float32)
    elif (THRESHOLD_01_LOW < ratio_21 < THRESHOLD_21_HIGH and
          THRESHOLD_01_LOW < ratio_01 < THRESHOLD_01_HIGH):
        fault_type = '2ф-З'
        one_hot = np.array([0, 0, 1, 0], dtype=np.float32)
    else:
        fault_type = 'неопределено'
        one_hot = np.array([0.25, 0.25, 0.25, 0.25], dtype=np.float32)

    return fault_type, one_hot, (ratio_21, ratio_01)


def classify_from_window(
    window_signals: np.ndarray,
    fs: float,
    f_net: float = 50.0,
    post_fault_ratio: float = 0.5,
) -> str:
    """Классификация вида КЗ из оконированного сигнала.

    Parameters
    ----------
    window_signals : np.ndarray, shape (12, T) или (6, T)
        Оконированный сигнал. Если 12 каналов — используются I1, I2, I0.
        Если 6 каналов — сначала вычисляются симметричные составляющие.
    fs : float
        Частота дискретизации, Гц.
    f_net : float
        Сетевая частота, Гц.
    post_fault_ratio : float
        Доля окна после момента КЗ для расчёта RMS (0.5 = вторая половина).

    Returns
    -------
    fault_type : str
        Классифицированный тип КЗ.
    """
    from symseq.instantaneous import fortescue_instantaneous

    n_channels, T = window_signals.shape

    if n_channels == 12:
        # Симметричные составляющие уже есть
        i1 = window_signals[3, :]  # I1
        i2 = window_signals[4, :]  # I2
        i0 = window_signals[5, :]  # I0
    elif n_channels == 6:
        # Вычисляем симметричные составляющие из фазных
        ia = window_signals[0, :]
        ib = window_signals[1, :]
        ic = window_signals[2, :]
        i0, i1, i2 = fortescue_instantaneous(ia, ib, ic, fs, f_net)
    else:
        raise ValueError(f"Expected 6 or 12 channels, got {n_channels}")

    # Расчёт RMS на пост-фазном участке
    post_start = int(T * (1.0 - post_fault_ratio))
    I1_rms = np.sqrt(np.mean(i1[post_start:] ** 2))
    I2_rms = np.sqrt(np.mean(i2[post_start:] ** 2))
    I0_rms = np.sqrt(np.mean(i0[post_start:] ** 2))

    fault_type, _, _ = classify_fault_type(I1_rms, I2_rms, I0_rms)
    return fault_type
