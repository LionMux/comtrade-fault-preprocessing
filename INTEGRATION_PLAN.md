# План интеграции пайплайна предобработки в Fault-Distance

> Этот документ описывает, как перенести код из `fault_location_preprocessing_pipeline.ipynb`
> в репозиторий https://github.com/LionMux/Fault-Distance

---

## Что уже есть в проекте (не трогаем)

| Файл | Что делает | Статус |
|------|-----------|--------|
| `symseq/core.py` | Фортескю для комплексных фазоров | OK Оставить |
| `symseq/fourier.py` | FFT-based симметричные составляющие | OK Оставить |
| `data/fault_inception.py` | Детекция момента КЗ (two-stage) | OK Оставить |
| `data/preprocessing.py` | Фильтрация Баттерворта, аугментация | OK Оставить |
| `tools/comtrade_to_csv.py` | COMTRADE → CSV конвертер | OK Оставить (6 каналов) |
| `models/cnn1d.py` | 1D-CNN модель | OK Оставить (принимает num_channels) |
| `models/resnet1d.py` | ResNet1D модель | OK Оставить (принимает num_channels) |

---

## Что нужно создать

### 1. `symseq/instantaneous.py` (НОВЫЙ)

Мгновенные симметричные составляющие по Фортескю (временной метод со сдвигом на T/3).

```python
"""
Мгновенные симметричные составляющие по Фортескю (временной метод).
"""
import numpy as np

def fortescue_instantaneous(ia, ib, ic, fs, f_net):
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
            i1[n] = i0[n]
        idx_b2 = n - 2 * k
        idx_c2 = n - k
        if idx_b2 >= 0 and idx_c2 >= 0:
            i2[n] = (ia[n] + ib[idx_b2] + ic[idx_c2]) / 3.0
        else:
            i2[n] = 0.0
    return i0, i1, i2

def fortescue_instantaneous_batch(signals, fs, f_net):
    signals = np.asarray(signals, dtype=np.float32)
    if signals.ndim == 2:
        ia, ib, ic = signals[:, 0], signals[:, 1], signals[:, 2]
        i0, i1, i2 = fortescue_instantaneous(ia, ib, ic, fs, f_net)
        return np.stack([i0, i1, i2], axis=1)
    elif signals.ndim == 3:
        N, C, T = signals.shape
        assert C == 3
        out = np.zeros((N, 3, T), dtype=np.float32)
        for n in range(N):
            ia, ib, ic = signals[n, 0, :], signals[n, 1, :], signals[n, 2, :]
            out[n, 0, :], out[n, 1, :], out[n, 2, :] = \
                fortescue_instantaneous(ia, ib, ic, fs, f_net)
        return out
    else:
        raise ValueError(f"Expected 2D or 3D input, got shape {signals.shape}")
```

**Куда вставить:** в папку `symseq/`, добавить импорт в `symseq/__init__.py`.

---

### 2. `data/fault_classifier.py` (НОВЫЙ)

Классификация вида КЗ по отношениям I2/I1 и I0/I1.

```python
"""
Классификация вида короткого замыкания (КЗ) по симметричным составляющим.
"""
import numpy as np
from typing import Tuple

THRESHOLD_21_LOW = 0.15
THRESHOLD_21_HIGH = 0.7
THRESHOLD_01_LOW = 0.25
THRESHOLD_01_HIGH = 0.7

FAULT_TYPES = ['3ф', '2ф', '2ф-З', '1ф-З', 'неопределено']

def classify_fault_type(I1_rms, I2_rms, I0_rms):
    ratio_21 = I2_rms / (I1_rms + 1e-10)
    ratio_01 = I0_rms / (I1_rms + 1e-10)
    if ratio_21 < THRESHOLD_21_LOW and ratio_01 < THRESHOLD_21_LOW:
        return '3ф', np.array([1, 0, 0, 0], dtype=np.float32), (ratio_21, ratio_01)
    elif ratio_21 > THRESHOLD_21_HIGH and ratio_01 < THRESHOLD_01_LOW:
        return '2ф', np.array([0, 1, 0, 0], dtype=np.float32), (ratio_21, ratio_01)
    elif ratio_21 > THRESHOLD_21_HIGH and ratio_01 > THRESHOLD_01_HIGH:
        return '1ф-З', np.array([0, 0, 0, 1], dtype=np.float32), (ratio_21, ratio_01)
    elif (THRESHOLD_01_LOW < ratio_21 < THRESHOLD_21_HIGH and
          THRESHOLD_01_LOW < ratio_01 < THRESHOLD_01_HIGH):
        return '2ф-З', np.array([0, 0, 1, 0], dtype=np.float32), (ratio_21, ratio_01)
    else:
        return 'неопределено', np.array([0.25, 0.25, 0.25, 0.25], dtype=np.float32), (ratio_21, ratio_01)

def classify_from_window(window_signals, fs, f_net=50.0):
    from symseq.instantaneous import fortescue_instantaneous
    n_channels, T = window_signals.shape
    if n_channels == 12:
        i1 = window_signals[4, :]
        i2 = window_signals[5, :]
        i0 = window_signals[6, :]
    elif n_channels == 6:
        ia, ib, ic = window_signals[0, :], window_signals[1, :], window_signals[2, :]
        i0, i1, i2 = fortescue_instantaneous(ia, ib, ic, fs, f_net)
    else:
        raise ValueError(f"Expected 6 or 12 channels, got {n_channels}")
    post_start = T // 2
    I1_rms = np.sqrt(np.mean(i1[post_start:] ** 2))
    I2_rms = np.sqrt(np.mean(i2[post_start:] ** 2))
    I0_rms = np.sqrt(np.mean(i0[post_start:] ** 2))
    fault_type, _, _ = classify_fault_type(I1_rms, I2_rms, I0_rms)
    return fault_type
```

**Куда вставить:** в папку `data/`.

---

## Что нужно изменить

### 3. `data/dataset.py` (ИЗМЕНИТЬ)

Добавить параметр `use_symseq: bool = False` в `__init__`.

После загрузки sig (после pad/trim):
```python
if use_symseq:
    from symseq.instantaneous import fortescue_instantaneous_batch
    sig_T = sig.T  # (6, T)
    i_batch = sig_T[0:3, :][np.newaxis, ...]  # (1, 3, T)
    u_batch = sig_T[3:6, :][np.newaxis, ...]  # (1, 3, T)
    i_seq = fortescue_instantaneous_batch(i_batch, file_fs_hz, f_net)  # (1, 3, T)
    u_seq = fortescue_instantaneous_batch(u_batch, file_fs_hz, f_net)  # (1, 3, T)
    sig = np.concatenate([sig, i_seq[0].T, u_seq[0].T], axis=1)  # (T, 12)
    self.num_channels = 12
```

Нормализация p.u. для 12 каналов:
```python
if self.num_channels == 12:
    self.signals[:, 0:3, :] /= Ibase_A   # IA, IB, IC
    self.signals[:, 3:6, :] /= Ibase_A   # I0, I1, I2
    self.signals[:, 6:9, :] /= Unom_kv   # UA, UB, UC
    self.signals[:, 9:12, :] /= Unom_kv  # U0, U1, U2
else:
    self.signals[:, 0:3, :] /= Ibase_A
    self.signals[:, 3:6, :] /= Unom_kv
```

---

### 4. `config.py` (ИЗМЕНИТЬ)

Добавить поля:
```python
USE_SYMSEQ: bool = True
ENSEMBLE_ENABLED: bool = False
FAULT_TYPES: list = ['3ф', '2ф', '2ф-З', '1ф-З', 'неопределено']
```

---

### 5. `train.py` (ИЗМЕНИТЬ)

Добавить аргумент:
```python
parser.add_argument('--fault-type', type=str, default='all',
                    choices=['all', '3ф', '2ф', '2ф-З', '1ф-З'])
```

В `_build_model`:
```python
num_ch = 12 if getattr(self.cfg, 'USE_SYMSEQ', False) else self.cfg.NUM_CHANNELS
return CNN1D(seq_length=self.cfg.SEQ_LENGTH, num_channels=num_ch, ...)
```

---

### 6. `inference.py` (ИЗМЕНИТЬ)

Добавить класс `EnsemblePredictor`:
- Этап 1: Классификация вида КЗ
- Этап 2: Выбор модели из checkpoints/{fault_type}/
- Этап 3: Предсказание расстояния

---

## Формат 12-канального тензора

```
Канал 0:  IA  (фазный ток A)
Канал 1:  IB  (фазный ток B)
Канал 2:  IC  (фазный ток C)
Канал 3:  I0  (нулевая последовательность)
Канал 4:  I1  (прямая последовательность)
Канал 5:  I2  (обратная последовательность)
Канал 6:  UA  (фазное напряжение A)
Канал 7:  UB  (фазное напряжение B)
Канал 8:  UC  (фазное напряжение C)
Канал 9:  U0  (нулевая последовательность)
Канал 10: U1  (прямая последовательность)
Канал 11: U2  (обратная последовательность)
```

Форма: `(12, SEQ_LENGTH)` — готов для `Conv1d(in_channels=12, ...)`.
