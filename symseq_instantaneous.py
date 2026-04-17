"""
Мгновенные симметричные составляющие по Фортескю (временной метод).

В отличие от symseq/core.py (комплексные фазоры), здесь используется
временной сдвиг на 1/3 периода для вычисления мгновенных значений
I0, I1, I2 и U0, U1, U2 непосредственно из осциллограмм.

Теория:
    i0(n) = (ia(n) + ib(n) + ic(n)) / 3
    i1(n) = (ia(n) + ib(n-k) + ic(n-2k)) / 3,  где k = fs / (3*f_net)
    i2(n) = (ia(n) + ib(n-2k) + ic(n-k)) / 3

Аналогично для напряжений.
"""

import numpy as np


def fortescue_instantaneous(ia, ib, ic, fs, f_net):
    """Вычисление мгновенных симметричных составляющих по Фортескю.

    Parameters
    ----------
    ia, ib, ic : np.ndarray, shape (T,)
        Фазные токи или напряжения (мгновенные значения).
    fs : float
        Частота дискретизации, Гц.
    f_net : float
        Сетевая частота, Гц (обычно 50.0 или 60.0).

    Returns
    -------
    i0, i1, i2 : np.ndarray, shape (T,)
        Нулевая, прямая и обратная последовательности.
    """
    L = len(ia)
    i0 = np.zeros(L, dtype=np.float32)
    i1 = np.zeros(L, dtype=np.float32)
    i2 = np.zeros(L, dtype=np.float32)

    k = int(fs / (3 * f_net))

    for n in range(L):
        i0[n] = (ia[n] + ib[n] + ic[n]) / 3.0

        idx_b1 = n - k
        idx_c1 = n - 2 * k
        if idx_b1 >= 0 and idx_c1 >= 0:
            i1[n] = (ia[n] + ib[idx_b1] + ic[idx_c1]) / 3.0
        else:
            i1[n] = i0[n]  # fallback на начальном участке

        idx_b2 = n - 2 * k
        idx_c2 = n - k
        if idx_b2 >= 0 and idx_c2 >= 0:
            i2[n] = (ia[n] + ib[idx_b2] + ic[idx_c2]) / 3.0
        else:
            i2[n] = 0.0

    return i0, i1, i2


def fortescue_instantaneous_batch(signals, fs, f_net):
    """Векторизованное вычисление мгновенных симметричных составляющих
    для батча сигналов.

    Parameters
    ----------
    signals : np.ndarray, shape (N, 3, T) или (T, 3)
        Батч трёхфазных сигналов.
        - Если (T, 3): одна трёхфазная осциллограмма [ia, ib, ic] по столбцам
        - Если (N, 3, T): N осциллограмм
    fs : float
        Частота дискретизации, Гц.
    f_net : float
        Сетевая частота, Гц.

    Returns
    -------
    seq_signals : np.ndarray
        Симметричные составляющие.
        - Если вход (T, 3): выход (T, 3) — [i0, i1, i2]
        - Если вход (N, 3, T): выход (N, 3, T) — [i0, i1, i2]
    """
    signals = np.asarray(signals, dtype=np.float32)

    if signals.ndim == 2:
        # (T, 3) → одна осциллограмма
        ia, ib, ic = signals[:, 0], signals[:, 1], signals[:, 2]
        i0, i1, i2 = fortescue_instantaneous(ia, ib, ic, fs, f_net)
        return np.stack([i0, i1, i2], axis=1)  # (T, 3)

    elif signals.ndim == 3:
        # (N, 3, T) → батч
        N, C, T = signals.shape
        assert C == 3, f"Expected 3 phases, got {C}"
        out = np.zeros((N, 3, T), dtype=np.float32)
        for n in range(N):
            ia, ib, ic = signals[n, 0, :], signals[n, 1, :], signals[n, 2, :]
            out[n, 0, :], out[n, 1, :], out[n, 2, :] =                 fortescue_instantaneous(ia, ib, ic, fs, f_net)
        return out

    else:
        raise ValueError(f"Expected 2D or 3D input, got shape {signals.shape}")
