#!/usr/bin/env python3
"""Консольная утилита: intent classification и slot tagging для ATIS (модели CNTK)."""

import os
import re
import shutil
import string
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# Паттерны для разбора строк CTF (atis.all.ctf)
_RE_S0_INDEX = re.compile(r"S0 (\d{1,3}):")
_RE_S0_WORD = re.compile(r"S0 \d{1,3}:1 \|# ([\w']+)")
_RE_S1 = re.compile(r"S1 (\d{1,2}):1 \|# (\w+)")
_RE_S2_INDEX = re.compile(r"S2 (\d{1,3}):")
_RE_S2_TAG = re.compile(r"S2 \d{1,3}:1 \|# ([\w\-\._]+)")


def find_cntk_binary() -> str | None:
    """Путь к исполняемому файлу CNTK: CNTK_BINARY, затем CNTK_HOME, затем PATH."""
    env_path = os.environ.get("CNTK_BINARY")
    if env_path:
        p = Path(env_path)
        if p.is_file():
            return str(p)
    home = os.environ.get("CNTK_HOME")
    if home:
        base = Path(home)
        for rel in (
            "cntk/cntk/CNTK.exe",
            "cntk/CNTK.exe",
            "CNTK.exe",
            "cntk",
        ):
            cand = base / rel
            if cand.is_file():
                return str(cand)
    for name in ("cntk", "CNTK.exe"):
        found = shutil.which(name)
        if found:
            return found
    return None


def load_vocabulary_and_labels(ctf_path: Path) -> tuple[dict[str, int], dict[str, str], dict[str, str]]:
    vocabulary: dict[str, int] = {}
    tags: dict[str, str] = {}
    types: dict[str, str] = {}
    with ctf_path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            m0 = _RE_S0_INDEX.search(line)
            mw = _RE_S0_WORD.search(line)
            if not m0 or not mw:
                continue
            word = mw.group(1)
            vocabulary[word] = int(m0.group(1))

            m1 = _RE_S1.search(line)
            if m1:
                types[m1.group(1)] = m1.group(2)

            m2i = _RE_S2_INDEX.search(line)
            m2t = _RE_S2_TAG.search(line)
            if m2i and m2t:
                tags[m2i.group(1)] = m2t.group(1)
    return vocabulary, tags, types


def main() -> int:
    cntk = find_cntk_binary()
    if not cntk:
        print(
            "Не найден исполняемый файл CNTK. Установите CNTK и добавьте его в PATH, "
            "либо задайте переменную окружения CNTK_BINARY (путь к бинарнику) "
            "или CNTK_HOME (каталог установки).",
            file=sys.stderr,
        )
        return 1

    atis_all = SCRIPT_DIR / "atis.all.ctf"
    if not atis_all.is_file():
        print(f"Не найден файл данных: {atis_all}", file=sys.stderr)
        return 1

    models_dir = SCRIPT_DIR / "Models"
    if not (models_dir / "slu_sentence_tagging.cmf").is_file() or not (
        models_dir / "slu_word_tagging.cmf"
    ).is_file():
        print(
            "Не найдены обученные модели в каталоге Models/. "
            "Сначала выполните обучение по инструкции в Python/README.md.",
            file=sys.stderr,
        )
        return 1

    vocabulary, tags, types = load_vocabulary_and_labels(atis_all)

    sentence_raw = sys.stdin.readline()
    tmp = "".join(
        c for c in sentence_raw if c.isalnum() or c in string.whitespace or c == "'"
    )
    sentence = tmp.lower().split()
    if not sentence:
        print("Пустой ввод: введите предложение на английском (одна строка).", file=sys.stderr)
        return 1

    unknown_words: list[bool] = []
    py_input = SCRIPT_DIR / "pyInput.ctf"
    with py_input.open("w", encoding="utf-8") as file:
        file.write("0\t|S0 178:1 |# BOS\n")
        for word in sentence:
            if word in vocabulary:
                idx = vocabulary[word]
                file.write(f"0\t|S0 {idx}:1 |# {word}\n")
                unknown_words.append(False)
            else:
                unknown_words.append(True)
        file.write("0\t|S0 179:1 |# EOS\n")

    cfg = "pyConfig.cntk"
    result = subprocess.run(
        [cntk, f"configFile={cfg}"],
        cwd=str(SCRIPT_DIR),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Ошибка при запуске CNTK:", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        return result.returncode or 1

    out_sentence = SCRIPT_DIR / "pyOutputSentenceTags.ctf.outputs"
    out_word = SCRIPT_DIR / "pyOutputWordTags.ctf.outputs"
    if not out_sentence.is_file() or not out_word.is_file():
        print(
            "Не созданы выходные файлы модели. Проверьте pyConfig.cntk и логи CNTK.",
            file=sys.stderr,
        )
        return 1

    with out_sentence.open(encoding="utf-8", errors="replace") as file:
        line = file.readline()

    try:
        probs = [int(float(x)) for x in line.split()]
        type_index = probs.index(1)
    except (ValueError, IndexError) as e:
        print(f"Не удалось разобрать выход intent-модели: {e!s}", file=sys.stderr)
        return 1

    word_tags: list[str] = []
    with out_word.open(encoding="utf-8", errors="replace") as file:
        file.readline()
        for unknown in unknown_words:
            if unknown:
                word_tags.append("O")
            else:
                wline = file.readline()
                if not wline:
                    word_tags.append("O")
                    continue
                try:
                    wprobs = [int(float(x)) for x in wline.split()]
                    word_tag_index = wprobs.index(1)
                    word_tags.append(tags[str(word_tag_index)])
                except (ValueError, KeyError):
                    word_tags.append("O")

    intent_key = str(type_index)
    intent_name = types.get(intent_key, intent_key)
    print("This sentence is about " + intent_name + ".")

    print("{0:<20}{1:<20}".format("Word: ", "Tag:"))
    for word, tag in zip(sentence, word_tags, strict=True):
        print("{0:<20}{1:<20}".format(word, tag))
    return 0


if __name__ == "__main__":
    sys.exit(main())
