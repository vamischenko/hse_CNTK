# Понимание естественного языка на Microsoft CNTK

Учебный проект (HSE): рекуррентные сети (LSTM) для **распознавания намерения (intent)** и **разметки слотов (slot tagging)** на корпусе [ATIS](https://www.microsoft.com/en-us/research/publication/an-introduction-to-computational-networks-and-the-computational-network-toolkit/) (Air Travel Information Services).

Официальный репозиторий CNTK: [github.com/Microsoft/CNTK](https://github.com/Microsoft/CNTK). Лицензия на использование библиотеки: [CNTK_LICENSE.md](CNTK_LICENSE.md).

> **Примечание.** CNTK с 2019 года не развивается активно; для новых проектов обычно выбирают PyTorch / TensorFlow / ONNX. Этот репозиторий сохранён как **архив учебной работы** и воспроизводимость зависит от установки устаревшего рантайма CNTK.

## Состав команды

- Кузнецов Владимир  
- Вороная Ксения  
- Куренков Евгений  

## Цель

По **англоязычному запросу** пользователя (в духе авиабронирования) определить:

1. **Intent** — о чём фраза (например, запрос рейса).  
2. **Slot tags** — BIO-разметка слов (город вылета, время и т.д.).

## Структура репозитория

| Каталог / файл | Содержание |
|----------------|------------|
| [Python/](Python/) | Консольная утилита `ATIS.py`, конфиги обучения и инференса, данные CTF, обученные модели в `Python/Models/`. |
| [ATIS/](ATIS/) | Материалы оригинального примера CNTK (конфиги, данные). |
| [Model comparison/](Model%20comparison/) | Сравнение вариантов архитектур из Hands-On Lab (логи и краткие метрики). |

## Установка CNTK

CNTK можно ставить из [релизов](https://github.com/Microsoft/CNTK/releases), через Docker-образы из [документации CNTK](https://github.com/Microsoft/CNTK/tree/master/Tools/docker) или готовый образ, например `docker pull torumakabe/cntk-cpu`.

На **Windows** часто нужны Visual C++ Redistributable 2013 и Microsoft MPI; на **Linux** — компилятор C++, Open MPI; для GPU — драйвер NVIDIA. В рамках проекта использовался **только CPU**.

## Запуск официальных примеров CNTK

После установки CNTK и клонирования примеров из репозитория CNTK:

```bash
cd Examples/Text/ATIS
cntk configFile=ATIS.cntk
```

Дополнительно: PennTreebank и др. примеры из `Examples/Text/`.

## Собственная утилита (`Python/`)

Скрипт читает одну строку со **stdin**, строит CTF-ввод, вызывает CNTK с `pyConfig.cntk` и печатает intent и теги по словам.

### Обучение моделей (один раз)

Из каталога `Python/`:

```bash
cntk configFile=SLUSentence.cntk
cntk configFile=SLUWord.cntk
```

В конфигах путь к данным задан как `$dataDir$/atis.all.ctf` (каталог запуска).

### Запуск приложения

```bash
cd Python
echo "i want to fly from boston to denver" | python3 ATIS.py
```

Скрипт ищет исполняемый файл CNTK в таком порядке:

1. переменная **`CNTK_BINARY`** — полный путь к `cntk` / `CNTK.exe`;  
2. **`CNTK_HOME`** — каталог установки (ищутся типичные подпути к бинарнику);  
3. **`PATH`** — команды `cntk` или `CNTK.exe`.

Подробности: [Python/README.md](Python/README.md).

## Документация и ссылки

- [Wiki CNTK](https://github.com/Microsoft/CNTK/wiki)  
- Введение: [An Introduction to Computational Networks and the Computational Network Toolkit](https://www.microsoft.com/en-us/research/publication/an-introduction-to-computational-networks-and-the-computational-network-toolkit/)  
- Презентация проекта (если есть в выдаче курса): `CNTK_language_understanding.pdf`  

---

*Проект выполнен в учебных целях (HSE).*
