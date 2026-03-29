# Python: SLU на базе CNTK

Пример консольного приложения по мотивам [SLU Hands-On](https://github.com/Microsoft/CNTK/tree/master/Examples/Tutorials/SLUHandsOn): натренированные рекуррентные сети (LSTM) для **классификации намерения** и **поштучной разметки слотов** на корпусе ATIS.

## Обучение моделей

Из **этого каталога** (чтобы `atis.all.ctf` и `Models/` пути совпали с конфигами):

```bash
cntk configFile=SLUSentence.cntk
cntk configFile=SLUWord.cntk
```

После обучения в `Models/` должны появиться:

- `slu_sentence_tagging.cmf` — intent;  
- `slu_word_tagging.cmf` — слоты.

## Запуск `ATIS.py`

Убедитесь, что CNTK доступен из командной строки или задайте окружение:

```bash
export CNTK_BINARY=/полный/путь/к/cntk   # Linux/macOS
# или на Windows: set CNTK_BINARY=C:\...\CNTK.exe
```

Запуск:

```bash
python3 ATIS.py
```

Введите **одну строку** на английском (лучше в тематике авиаперевозок), завершите ввод (Enter). Либо:

```bash
echo "what flights from pittsburgh to baltimore" | python3 ATIS.py
```

Скрипт использует только стандартную библиотеку Python 3; рабочий каталог определяется автоматически (не нужно править пути в коде).

## Файлы

| Файл | Назначение |
|------|------------|
| `ATIS.py` | Входной конвейер и вызов CNTK |
| `atis.all.ctf` | Данные для построения словаря и обучения |
| `pyConfig.cntk` | Инференс (запись выходов `pyOutput*.ctf`) |
| `pyInput.ctf`, `pyOutput*.ctf*` | Временные файлы (можно удалять после запуска) |
