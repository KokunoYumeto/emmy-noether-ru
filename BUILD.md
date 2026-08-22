# Сборка / Build

Требования: Python 3, XeLaTeX, пакет Python `pypdf`. Распакуйте архив без изменения структуры и выполните из его корня:

```text
python build_ru_release_v001_edit0017.py --build
python audit_ru_release_v001_edit0017.py
```

Скрипт сборки проверяет размеры и SHA-256 четырёх TeX-файлов и изображения, выполняет по два последовательных прохода XeLaTeX без shell escape и создаёт четыре компонентных PDF и полный A4-читатель. Аудит ожидает сохранённую структуру полного рабочего выпуска; его исходник и зафиксированный публичный результат находятся в архиве доказательств.

Requirements: Python 3, XeLaTeX, and Python package `pypdf`. From the extracted archive root, run the two commands above. The builder authenticates the four TeX files and image by byte count and SHA-256, runs two serial XeLaTeX passes without shell escape, and creates the four component PDFs plus the complete A4 reader.
