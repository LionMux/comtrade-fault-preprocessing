# COMTRADE Fault Preprocessing Pipeline

> Пайплайн предобработки осциллограмм COMTRADE (IEEE C37.111) для задачи локализации короткого замыкания (КЗ) с помощью машинного обучения.

---

## Описание

Jupyter Notebook `fault_location_preprocessing_pipeline.ipynb` реализует полный end-to-end цикл обработки одного COMTRADE-файла от сырых данных до готового тензора для нейросети:

1. **Парсинг COMTRADE** — чтение `.cfg` (метаданные) и `.dat` (осциллограмма).
2. **Фильтрация** — удаление постоянного смещения нуля (DC offset) методом скользящего среднего за период сетевой частоты.
3. **Детекция момента КЗ** — по производной тока с порогом `eta * Inom`.
4. **Оконирование** — вырезание окна `[-50 мс, +150 мс]` относительно момента КЗ с zero-padding.
5. **Симметричные составляющие (Фортескю)** — вычисление `I₀, I₁, I₂` и `U₀, U₁, U₂`.
6. **Классификация вида КЗ** — по отношениям `I₂/I₁` и `I₀/I₁` определяется тип: `3ф`, `2ф`, `2ф-З`, `1ф-З`.
7. **Нормализация в p.u.** — приведение токов и напряжений к относительным единицам.
8. **Формирование тензора** — сборка `X ∈ R^(10 × L_window)` и целевой переменной `y`.

---

## Структура проекта

```
.
├── fault_location_preprocessing_pipeline.ipynb   # Основной notebook
├── data/
│   ├── 3.1.1(K3, 1A).cfg                         # Исходный COMTRADE (конфиг)
│   └── 3.1.1(K3, 1A).dat                         # Исходный COMTRADE (данные)
├── filtered_data.cfg                             # Результат фильтрации (конфиг)
├── filtered_data.dat                             # Результат фильтрации (данные)
├── fault_sample_processed.npz                    # Готовый тензор X и метка y
├── .agents/skills/                               # Kimi Code CLI skills
│   ├── auto-orchestrator/
│   ├── code-style/
│   ├── fault-distance/
│   ├── ml-research/
│   └── web-dev/
├── AGENTS.md                                     # Инструкции для AI-агентов
├── README.md                                     # Этот файл
├── requirements.txt                              # Зависимости Python
└── LICENSE                                       # MIT License
```

---

## Установка

```bash
pip install -r requirements.txt
```

Или внутри notebook:

```python
!pip install numpy pandas matplotlib scipy comtrade
```

---

## Использование

1. Откройте `fault_location_preprocessing_pipeline.ipynb` в Jupyter Notebook / JupyterLab.
2. Запустите все ячейки последовательно.
3. В разделе 7 задайте вручную `FAULT_DISTANCE_KM` для расчёта целевой переменной `y` в p.u.
4. Результат сохраняется в `fault_sample_processed.npz`.

---

## Данные

- **Файл:** `data/3.1.1(K3, 1A).cfg` / `.dat`
- **Источник:** RTDS Technologies (симуляция)
- **Формат:** COMTRADE 1999, ASCII
- **Каналы:** 59 аналоговых + 28 дискретных
- **Частота дискретизации:** 5000 Гц
- **Количество отсчётов:** 50000

---

## Kimi Code CLI Skills

В директории `.agents/skills/` находятся skills для автоматизации работы с проектом:

- `auto-orchestrator` — оркестрация многошаговых workflow
- `fault-distance` — специфичные правила для дипломного проекта Fault-Distance
- `ml-research` — workflow для ML-экспериментов
- `code-style` — универсальные правила стиля кода
- `web-dev` — правила веб-разработки

---

## Лицензия

MIT License — см. [LICENSE](LICENSE).
