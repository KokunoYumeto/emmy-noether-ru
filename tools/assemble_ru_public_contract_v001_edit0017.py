#!/usr/bin/env python3
"""Assemble the deterministic public contract for NOETHER-RU RU001-EDIT-0017.

The output is deliberately human-facing and finite: one reader, one editable
source archive, one evidence/provenance archive, one SHA-256 manifest, and a
complete standalone GitHub tree.  Internal session logs and temporary build
trees are not public release material.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VERSION = "2026.08.22-r2"
RELEASE_DATE = "2026-08-22"
RELEASED_AT = "2026-08-22T00:00:00Z"
CONCEPT_DOI = "10.5281/zenodo.21926366"
GLOBAL_DOI = "10.5281/zenodo.20412587"
GERMAN_DOI = "10.5281/zenodo.21940320"
GERMAN_AUTHORITY = {
    "authority_id": "NOETH-DE-ED-0015",
    "bytes": 2154017,
    "sha256": "51A25101C04877AE740989E72B2AD65A7A7E65B081077C4A518BF1737AD5B907",
}
REPOSITORY = "https://github.com/KokunoYumeto/emmy-noether-ru"
RELEASE_FILENAMES = (
    "00_NOETHER_RUSSIAN_COMPLETE_LINKED_READER.pdf",
    "01_NOETHER_RUSSIAN_EDITABLE_SOURCES.zip",
    "02_NOETHER_RUSSIAN_EVIDENCE_AND_PROVENANCE.zip",
    "03_NOETHER_RUSSIAN_SHA256_MANIFEST.txt",
)

PINNED_INPUTS = {
    "source/base-papers1-43-ru.tex": (
        2854276,
        "D53F4E0E1D24623B353A562480A53BE8478BB6CB39BBDC36ED0E820D73495B9A",
    ),
    "source/44-book-ru.tex": (
        245150,
        "E90E13D0013ABC5BADED8AD0785CF8099C33557EAECBED06F6BB657F985606CF",
    ),
    "source/45-ru.tex": (
        37143,
        "06DC908C13904FFF06C6638D6F5DC192E29EFD8C3CFC9C6F6F7A34F61A812F48",
    ),
    "source/bib-ru.tex": (
        13037,
        "A1EEC412E8B5E1DC67CEC37F510F25E451017E67ADDC7F7D50DAE6EBF2606276",
    ),
    "assets/authority_rosette_native_supported_mask.png": (
        797,
        "B2AF3955A8255B4A6D925E174B7B81311C64C669CE21B07E75002494E55F2FF5",
    ),
    "release_v001_edit0017/source/emmy-noether-russian-v001-edit0017.tex": (
        397,
        "60179DE2829BE256FFB141A6B07BD58C38513A7B386F931EE89A06CD775A5482",
    ),
    "release_v001_edit0017/pdf/emmy-noether-russian-v001-edit0017.pdf": (
        3419673,
        "976B0AEC3FFAC0E26AFA28C962606A40B94492AB6DCFE3A9454F5362CF969FF4",
    ),
    "release_v001_edit0017/evidence/build-manifest.json": (
        12715,
        "9EE862038B5FC71F0EA56010733AD4F3D7E6AE64C54AF11774D8ECEF235BCD9B",
    ),
    "release_v001_edit0017/evidence/RELEASE_AUDIT_VISUAL_QA_RU001_EDIT0017.json": (
        6863,
        "8C3CA9591AA68A08D6E2E56C08B4C724D0F4D3A7E728C5E034DBA644003626BE",
    ),
    "RUSSIAN_DECISIONS_v001.jsonl": (
        28864,
        "4469369DCA60F66F82E2AF9B81FCC72CAE24A665C46AAB3FF8B6D4D0B2EDFED3",
    ),
    "machine_index/LANGUAGE_EDITION_INDEX.json": (
        6637,
        "6389D8A78BDD4CD57EC096B8D6E5C2DC384674AB315E3E7A875FF1B792C2A99B",
    ),
    "machine_index/README.md": (
        852,
        "9387C610BDD68F220FB48251336B5F70F4B0F50991F21E91D1FA9515FC2BEF50",
    ),
    "reference_sources/INDEX.json": (
        6029,
        "89366DAED44759BA64ECD94F4B458E4A939D15AF004BECF9BB19E5822146BB29",
    ),
    "reference_sources/README.md": (
        814,
        "AFBB6F57CF9D034195F9EABE1F27A231DA351622F3DD7A1CBF58D94ED2718A05",
    ),
}

TOOL_PINS = {
    "apply_ru_ed0014_source_fidelity_tranche_v001.py": (47328, "D1A6351713247EBC4D4E58BAC3EA70A745AAF503B6F3F56C1001239A2F38FE9E"),
    "apply_ru_ed0015_p45_notation_fidelity_v001.py": (59651, "72BF4C9F1FF8A0A8801747728CDB3386384BF9A1595509ED12578A2D124E59EE"),
    "apply_ru_p02_five_column_rosette_v001.py": (50447, "411DB858FDFE3B32337F026F4C8221BB64FCAE55B53AA3056058913EBB8AB0DE"),
    "apply_ru_p14_singular_primary_numbers_v001.py": (12827, "09078408356AC623D9C5234450C08DD8EE61D773B8F939B327379A1C51E8289B"),
    "apply_ru_p18_p19_primary_register_v001.py": (44655, "AE8EF885BC28020866D9F82509A732DC488C0516B08EE3B54541C8BA2C3CBEDA"),
    "apply_ru_p24_citation_placement_v001.py": (28395, "B6C066D2B334888AAD44C85751DC4433A180E8982F1526731A71815C2E38AD8C"),
    "apply_ru_p24_ed0013_repairs_v001.py": (14043, "8AEA8390781E26D94DA1B5889C8FD0AA5C71E7FAB7ADD3382382E01096E610E7"),
    "apply_ru_p24_formula3_norm_repairs_v001.py": (13415, "4302C81497080AF2B8423D8B795E371B3BE31E3B513C932CE714A9D7DC3E9532"),
    "apply_ru_p24_idealbasis_family_v001.py": (11815, "07B63699A141EEAB31B00B22C87AB469EA46306EE7F01698D7D92F6AF80A2D63"),
    "apply_ru_p24_label_geometry_v001.py": (13745, "E5E5F01329F107A1E0337BC6E0FE6681D64CE64CB4DE64FB81D8D6C42AB2D64F"),
    "apply_ru_p24_primary_register_v001.py": (27536, "5D4B8490AEC0E0A61BFC8DCCD29CFA920E19CFD906F5E9C1C6236FADD9B28BF2"),
    "apply_ru_p30_coefficient_ideal_fidelity_v001.py": (26057, "79AA0DD50662D4B449BED2970C0363059E95C865E8238D20FDDBCEAB0D37D40B"),
    "apply_ru_p30_section08_n_congruence_v001.py": (57852, "2C511FEE0B978834DB26AF9A0AD74F75C3D5A61F801F282860F9E2C8ED3820DD"),
    "apply_ru_p45_math_annalen_rebase_v001.py": (56072, "AE50E1330C31A9B43564203D7822DA715F4FB5F936441C7C41E42BB2B821332A"),
    "apply_ru_p45_primary_register_v001.py": (32498, "BE8DC8C5AE95259742817B488DAF6C11036206D62B45E0340C5AD7BA8038BBEB"),
    "apply_ru_p45_redundant_label_v001.py": (27548, "E0A0D894AA0AE0C696D017C8D2E5F1A66897C46362CA3FC69CA1134EAA0679B3"),
    "apply_ru_portable_provenance_locators_v001.py": (7468, "15AD1781FBB35B7CEF207FCD77C944B67F2591099B76A7FD839656786617E215"),
    "audit_ru_release_v001_edit0017.py": (18681, "0FF9C7BBDC6C9BEB95F69C09F8A49A4E1BFDCAC53922C175FEBB7809D9AEFAB1"),
    "build_ru_release_v001_edit0017.py": (12241, "1F275836E418252E4D9D2F8D8F7A1C17E1418EB98727E445E8473396D4645696"),
}

# Only these tools are already portable as public executables.  Historical
# applicators remain authenticated above and are represented by exact hashes;
# their private custody paths are not copied to the public release.
PUBLIC_TOOL_NAMES = (
    "build_ru_release_v001_edit0017.py",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def record(path: Path, relative_to: Path) -> dict:
    return {
        "path": path.relative_to(relative_to).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def text_bytes(value: str) -> bytes:
    return value.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def portable_public_text(relative: str, data: bytes) -> tuple[bytes, dict | None]:
    """Replace private Windows custody roots in a public evidence copy.

    The canonical file is never changed.  The returned map pins both the
    canonical input and the public derivative so the transformation is
    auditable without publishing a local account name or home-directory path.
    """

    text = data.decode("utf-8")
    original = data
    replacements = 0
    patterns = (
        (re.compile(r"C:/Users/[^/\\\s\"']+/Documents/interlanguage/", re.I), "interlanguage-workspace://"),
        (re.compile(r"C:\\\\Users\\\\[^\\]+\\\\Documents\\\\interlanguage\\\\", re.I), "interlanguage-workspace://"),
        (re.compile(r"C:\\Users\\[^\\]+\\Documents\\interlanguage\\", re.I), "interlanguage-workspace://"),
        (re.compile(r"C:/Users/[^/\\\s\"']+/", re.I), "user-filesystem://"),
        (re.compile(r"C:\\\\Users\\\\[^\\]+\\\\", re.I), "user-filesystem://"),
        (re.compile(r"C:\\Users\\[^\\]+\\", re.I), "user-filesystem://"),
        (re.compile(r"C:/Users/[^/\\\s\"']+", re.I), "user-filesystem://"),
        (re.compile(r"C:\\\\Users\\\\[^\\\s\"']+", re.I), "user-filesystem://"),
        (re.compile(r"C:\\Users\\[^\\\s\"']+", re.I), "user-filesystem://"),
    )
    for pattern, replacement in patterns:
        text, count = pattern.subn(replacement, text)
        replacements += count
    public = text_bytes(text)
    if public == original:
        return public, None
    return public, {
        "path": relative,
        "policy": "private Windows custody root to logical public locator; canonical bytes retained only in controlled workspace",
        "replacements": replacements,
        "canonical": {"bytes": len(original), "sha256": sha256_bytes(original)},
        "public_copy": {"bytes": len(public), "sha256": sha256_bytes(public)},
    }


def write_exact(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to replace existing output: {path}")
    path.write_bytes(data)
    if path.read_bytes() != data:
        raise RuntimeError(f"write readback mismatch: {path}")


def authenticate_inputs() -> None:
    failures: list[str] = []
    for relative, expected in {**PINNED_INPUTS, **TOOL_PINS}.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing {relative}")
            continue
        actual = (path.stat().st_size, sha256(path))
        if actual != expected:
            failures.append(f"pin mismatch {relative}: expected {expected}, got {actual}")
    if failures:
        raise RuntimeError("\n".join(failures))

    ledger_lines = (ROOT / "RUSSIAN_DECISIONS_v001.jsonl").read_text(encoding="utf-8").splitlines()
    ledger = [json.loads(line) for line in ledger_lines]
    if len(ledger) != 17 or len({row["decision_id"] for row in ledger}) != 17:
        raise RuntimeError("decision ledger is not the sealed 17-row monotonic sequence")
    if ledger[-1]["decision_id"] != "RU001-EDIT-0017":
        raise RuntimeError("decision ledger head mismatch")
    for number in range(1, 18):
        sidecar = ROOT / "decision_records" / f"RU001-EDIT-{number:04d}.json"
        if not sidecar.is_file():
            raise FileNotFoundError(sidecar)
        json.loads(sidecar.read_text(encoding="utf-8"))


def portable_machine_index(version_doi: str) -> dict:
    index = json.loads((ROOT / "machine_index/LANGUAGE_EDITION_INDEX.json").read_text(encoding="utf-8"))
    index["schema"] = "interlanguage-language-edition-index/1.1-public"
    index["updated_at"] = RELEASED_AT
    index["work"]["published_predecessor_version_doi"] = "10.5281/zenodo.21926367"
    index["work"]["current_version_doi"] = version_doi
    index["canonical_lane_head"]["ledger"]["path"] = "evidence/RUSSIAN_DECISIONS_v001.jsonl"
    index["canonical_lane_head"]["head_record"]["path"] = "evidence/decisions/RU001-EDIT-0017.json"
    for item in index["editable_sources"]:
        item["path"] = "source/" + Path(item["path"]).name
    index["derived_reader"]["path"] = "reader/" + RELEASE_FILENAMES[0]
    index["derived_reader"]["build_manifest"]["path"] = "evidence/build-manifest.json"
    index["derived_reader"]["release_audit"]["path"] = "evidence/RELEASE_AUDIT_VISUAL_QA_RU001_EDIT0017.json"
    index["release"] = {
        "version": VERSION,
        "publication_date": RELEASE_DATE,
        "concept_doi": CONCEPT_DOI,
        "version_doi": version_doi,
        "repository": REPOSITORY,
        "public_record": f"https://zenodo.org/records/{version_doi.rsplit('.', 1)[-1]}",
        "artifact_contract": list(RELEASE_FILENAMES),
    }
    return index


def readme(version_doi: str) -> str:
    record_id = version_doi.rsplit(".", 1)[-1]
    reader_url = f"https://zenodo.org/records/{record_id}/files/{RELEASE_FILENAMES[0]}"
    return f"""# Эмми Нётер: полное русское издание корпуса

[Читать полный 609-страничный PDF]({reader_url}) · [стабильный DOI русского издания](https://doi.org/{CONCEPT_DOI}) · [DOI этой версии](https://doi.org/{version_doi})

Это полное поддерживаемое русское издание корпуса работ Эмми Нётер: статьи 1–43, лекции 1929/30 года о гиперкомплексных величинах (работа 44), статья 45 и русская библиография. Редактируемые исходники, решения, инструменты воспроизведения, результаты сборки и проверки опубликованы вместе с книгой.

## Что содержит версия {VERSION}

- 609 страниц формата A4; четыре самостоятельно собираемых компонента: 550 + 47 + 7 + 5 страниц.
- Исправления верности немецкому источнику и математической записи, в том числе восстановление исторического термина «сингулярные примарные числа» там, где немецкий текст различает *Primarzahl* и *Primzahl*.
- 17 последовательных, обратимо воспроизводимых редакционных решений; открытых блокировок и неразрешённых редакционных диспозиций — 0.
- Две независимые чистые сборки дали побайтно одинаковые PDF; проверены структура TeX, формулы, ссылки, шрифты, извлечённый текст и контрольные страницы.
- Все внутренние пути заменены переносимыми логическими локаторами; машинная точка входа — [`machine/LANGUAGE_EDITION_INDEX.json`](machine/LANGUAGE_EDITION_INDEX.json).

Это машинно-ассистированное научное рабочее издание, а не рецензированное критическое издание и не свидетельство проверки носителями русского языка. Отсутствие внешней и общественной языковой рецензии раскрыто и не скрывается за техническими тестами.

## Публичные файлы

1. `00_...pdf` — полный читательский PDF.
2. `01_...zip` — редактируемые TeX-исходники, ресурс изображения, инструкции сборки и машинный индекс.
3. `02_...zip` — журнал решений, доказательства происхождения, методика, инструменты воспроизведения и QA.
4. `03_...txt` — SHA-256 и размеры первых трёх файлов.

Немецкая проектная опора: `NOETH-DE-ED-0015`, [DOI {GERMAN_DOI}](https://doi.org/{GERMAN_DOI}). Глобальный многоязычный каталог: [DOI {GLOBAL_DOI}](https://doi.org/{GLOBAL_DOI}). Границы прав описаны в [`LICENSE`](LICENSE).

---

# Emmy Noether: Complete Russian Corpus Edition

[Read the complete 609-page PDF]({reader_url}) · [stable Russian concept DOI](https://doi.org/{CONCEPT_DOI}) · [this version DOI](https://doi.org/{version_doi})

This is the complete maintained Russian edition: Papers 1–43, the 1929/30 lectures on hypercomplex quantities (Work 44), Paper 45, and the Russian bibliography. Version {VERSION} seals 17 reversible editorial decisions, portable provenance locators, two byte-identical clean builds, source/math/link/font/text checks, and visual review of the changed locus and every component boundary. There are no open editorial holds.

It is a machine-assisted scholarly working edition, not a peer-reviewed critical edition and not a claim of native-speaker certification. Editable sources, replay tools, evidence, and the public machine index accompany the reader. Rights limitations and third-party boundaries remain explicit.
"""


def methodology() -> str:
    return f"""# Методика русской редакции / Russian-edition methodology

## Русская версия

### 1. Что считается опорой

Редакционная опора этой линии — немецкий проектный корпус `NOETH-DE-ED-0015` ({GERMAN_AUTHORITY['sha256']}). Он служит контрольным объектом для структуры, формул и смысла, но не объявляется критическим немецким изданием. Русские версии являются переводными свидетелями этой редакции; они не превращаются в общий «канон русского математического языка».

### 2. Как принимались решения

Каждая содержательная правка получила последовательный номер `RU001-EDIT-....`, точный локатор, текст или формулу до и после, роли источников, отвергнутые варианты, оценку неопределённости и обратное преобразование. Локальная терминологическая литература применялась только в своей предметной области. Сходство с другим переводным языком не считалось само по себе русским авторитетом.

### 3. Роль ИИ

OpenAI Codex помогал находить расхождения, формулировать кандидаты, собирать доказательства, выполнять детерминированные преобразования и технические проверки. ИИ не заменён ярлыком «проверено человеком»: внешняя, общественная и носительская рецензия не проводилась. Поэтому публикация честно называет себя машинно-ассистированным рабочим изданием.

### 4. Воспроизводимость

Исходные свидетели не переписывались задним числом. Преобразования имеют побайтные предшественники и обратный ход; 17-строчный журнал решений задаёт порядок. Четыре TeX-источника и один графический ресурс закреплены длиной и SHA-256. Приватные пути удалены из комментариев и заменены схемой `noether-corpus://corpus/`, разрешаемой через публичный машинный индекс.

Публичные копии ранних боковых записей решений дополнительно заменяют локальные корни хранения логическими URI. `PUBLIC_COPY_TRANSFORMATIONS.json` сохраняет длину и SHA-256 как исходной канонической записи, так и публичной копии. Старые аппликаторы с локальными путями не выдаются за переносимые программы: их точные исходные хэши опубликованы отдельно, а переносимыми исполняемыми инструментами выпуска являются сборщик и упаковщик.

### 5. Сборка и проверка

Каждый компонент дважды последовательно собирался XeLaTeX без shell escape, затем объединялся в A4-читатель. Две чистые сборки побайтно совпали. Выпуск заблокирован при отсутствующем знаке, неопределённой ссылке или цитате, повторной метке либо несовпадении числа страниц. Все 609 страниц проверены на равенство потока содержимого и извлечённого текста с предшественником после чисто прованансной правки; отдельно просмотрены страницы 1, 200–202, 550–551, 597–598, 604–605 и 609. Все шрифты встроены и подмножественны; традиционное ограничение ToUnicode у математических символьных шрифтов раскрыто.

### 6. Публикационная граница

PDF — производный результат, а не независимый переводный свидетель. CC0 применяется только к тем переводам, набору, метаданным, инструментам и доказательствам, на которые проект вправе распространить такое посвящение. Оригинальные работы, немецкий редакционный материал, факсимиле, шрифты, программы и другие сторонние объекты сохраняют собственный правовой статус.

## English counterpart

The project German authority is `NOETH-DE-ED-0015`; it controls structure, formulas, and intended meaning but is not claimed as a critical German edition. Every substantive Russian change has a monotonic `RU001-EDIT-....` record with exact locators, before/after payloads, evidence roles, rejected alternatives, uncertainty, and reverse replay. Domain terminology sources are used only within their evidentiary scope; other translation lanes are comparators, not native-Russian authority.

OpenAI Codex assisted with discrepancy detection, candidate formulation, evidence assembly, deterministic transformation, and technical QA. No external, community, or native-speaker review is claimed. Four pinned TeX sources and one pinned image build serially with two XeLaTeX passes and no shell escape. Two clean builds are byte-identical; structural, math, reference, citation, label, font, text-extraction, cross-head page, and targeted visual gates pass. The public machine index makes the edition discoverable and replayable without private filesystem paths. The PDF is a derived artifact, not an independent translation witness, and the rights boundary above remains controlling.

Public copies of early decision sidecars replace local custody roots with logical URIs. `PUBLIC_COPY_TRANSFORMATIONS.json` pins canonical and public-copy hashes. Historical applicators that embed local custody paths are represented by exact source hashes rather than misrepresented as portable executables; the current builder and package assembler are portable.
"""


def build_instructions() -> str:
    return """# Сборка / Build

Требования: Python 3, XeLaTeX, пакет Python `pypdf`. Распакуйте архив без изменения структуры и выполните из его корня:

```text
python build_ru_release_v001_edit0017.py --build
python audit_ru_release_v001_edit0017.py
```

Скрипт сборки проверяет размеры и SHA-256 четырёх TeX-файлов и изображения, выполняет по два последовательных прохода XeLaTeX без shell escape и создаёт четыре компонентных PDF и полный A4-читатель. Аудит ожидает сохранённую структуру полного рабочего выпуска; его исходник и зафиксированный публичный результат находятся в архиве доказательств.

Requirements: Python 3, XeLaTeX, and Python package `pypdf`. From the extracted archive root, run the two commands above. The builder authenticates the four TeX files and image by byte count and SHA-256, runs two serial XeLaTeX passes without shell escape, and creates the four component PDFs plus the complete A4 reader.
"""


def license_text() -> str:
    return """CC0 1.0 Universal dedication applies only to the extent rights exist in project-created translation, typesetting, metadata, manifests, tools, and evidence. Emmy Noether's original works, German editorial material, facsimiles, fonts, software, and other third-party material are not relicensed and retain their own legal status and licenses.

Посвящение CC0 1.0 Universal применяется лишь в той мере, в какой проект обладает правами на созданные им перевод, набор, метаданные, манифесты, инструменты и доказательства. Оригинальные работы Эмми Нётер, немецкий редакционный материал, факсимиле, шрифты, программы и другие сторонние материалы не перелицензируются и сохраняют собственный правовой статус и лицензии.
"""


def citation_cff(version_doi: str) -> str:
    return f'''cff-version: 1.2.0
message: "При использовании издания цитируйте предпочтительную библиографическую запись. / If you use this edition, cite the preferred citation."
title: "Эмми Нётер: полное русское издание корпуса"
type: dataset
authors:
  - family-names: Noether
    given-names: Emmy
version: "{VERSION}"
date-released: "{RELEASE_DATE}"
url: "https://doi.org/{version_doi}"
preferred-citation:
  type: book
  title: "Эмми Нётер: полное русское издание корпуса / Emmy Noether: Complete Russian Corpus Edition"
  authors:
    - family-names: Noether
      given-names: Emmy
  doi: "{version_doi}"
  version: "{VERSION}"
  date-released: "{RELEASE_DATE}"
  languages:
    - "ru"
'''


def coverage_tsv() -> str:
    return """component\tcoverage\tpages\tartifact\tproject_authority
Статьи 1–43 / Papers 1–43\tcomplete\t550\tbase-papers1-43-ru.tex\tNOETH-DE-ED-0015
Лекции 1929/30 / Work 44\tcomplete\t47\t44-book-ru.tex\tNOETH-DE-ED-0015
Статья 45 / Paper 45\tcomplete\t7\t45-ru.tex\tNOETH-DE-ED-0015
Библиография / Bibliography\tcomplete\t5\tbib-ru.tex\tNOETH-DE-ED-0015
"""


def limitations_tsv() -> str:
    return """item_id\tstatus\tdescription
GENERAL-001\tdisclosed\tМашинно-ассистированное научное рабочее издание; последующие исправления публикуются новыми версиями. / Machine-assisted scholarly working edition; later corrections are released as successor versions.
REVIEW-001\tnot_completed_not_a_gate\tНет заявления о внешней, общественной или носительской сертификации русского текста. / No external, community, or native-speaker certification is claimed.
CRITICAL-001\tnot_claimed\tНи немецкая опора проекта, ни русский перевод не объявляются критическим изданием. / Neither the project German authority nor this Russian translation is claimed as a critical edition.
OPEN-HOLDS\tzero\tНа голове RU001-EDIT-0017 нет открытых редакционных блокировок или диспозиций. / No open editorial holds or dispositions at RU001-EDIT-0017.
MATH-FONT-001\tdisclosed\tТрадиционные математические символьные шрифты не везде имеют ToUnicode; текстовые и кириллические шрифты его имеют. / Traditional math-symbol fonts do not all carry ToUnicode; text and Cyrillic fonts do.
"""


def datacite_relations(version_doi: str) -> dict:
    return {
        "schema": "noether-language-datacite-relations/1.1",
        "language": {"bcp47": "ru", "script": "Cyrl", "name": "Russian / русский"},
        "language_concept_doi": CONCEPT_DOI,
        "exact_release_doi": version_doi,
        "relations": [
            {"subject": CONCEPT_DOI, "relationType": "IsPartOf", "object": GLOBAL_DOI},
            {"subject": version_doi, "relationType": "IsVersionOf", "object": CONCEPT_DOI},
            {"subject": version_doi, "relationType": "IsDerivedFrom", "object": GERMAN_DOI},
            {"subject": version_doi, "relationType": "IsSupplementedBy", "object": REPOSITORY},
        ],
        "translation_semantics": {
            "intended_relation": "IsTranslationOf",
            "object": {"doi": GERMAN_DOI, **GERMAN_AUTHORITY},
            "note": "The precise translation relation is preserved here and in prose; the public Zenodo relation uses IsDerivedFrom where its form vocabulary requires a supported relation.",
        },
    }


def zenodo_metadata(version_doi: str) -> dict:
    record_id = version_doi.rsplit(".", 1)[-1]
    reader_url = f"https://zenodo.org/records/{record_id}/files/{RELEASE_FILENAMES[0]}"
    description = (
        f'<p><strong><a href="{reader_url}">Читать полное 609-страничное русское издание</a></strong> / '
        f'<a href="{reader_url}?download=1">скачать PDF</a>.</p>'
        f'<p>Полное поддерживаемое русское издание корпуса Эмми Нётер: статьи 1–43, лекции 1929/30 года о гиперкомплексных величинах (работа 44), статья 45 и русская библиография. Версия {VERSION} закрепляет 17 последовательных обратимо воспроизводимых редакционных решений, переносимые локаторы происхождения и две побайтно одинаковые чистые сборки. Проверены структура TeX, математическая запись, ссылки, шрифты, извлечённый текст и контрольные страницы; открытых редакционных блокировок нет.</p>'
        '<p>Это машинно-ассистированное научное рабочее издание, а не рецензированное критическое издание и не свидетельство проверки носителями русского языка. Редактируемые исходники, решения, инструменты воспроизведения, QA и машинный индекс опубликованы вместе с книгой.</p>'
        f'<p>Стабильный DOI русского издания: <a href="https://doi.org/{CONCEPT_DOI}">{CONCEPT_DOI}</a>; DOI этой версии: <a href="https://doi.org/{version_doi}">{version_doi}</a>. Немецкая проектная опора: <a href="https://doi.org/{GERMAN_DOI}">NOETH-DE-ED-0015</a>; глобальный многоязычный каталог: <a href="https://doi.org/{GLOBAL_DOI}">{GLOBAL_DOI}</a>; исходники: <a href="{REPOSITORY}">{REPOSITORY}</a>.</p>'
        f'<hr><p><strong>English.</strong> This complete maintained Russian edition covers Papers 1–43, the 1929/30 hypercomplex-quantities lectures, Paper 45, and the Russian bibliography. Version {VERSION} seals 17 reversible editorial decisions, portable provenance locators, two byte-identical clean builds, and passing TeX/math/link/font/text/visual QA, with zero open editorial holds. It is a machine-assisted scholarly working edition, not a peer-reviewed critical edition and not a claim of native-speaker certification. Editable sources, replay tools, provenance, and the public machine index accompany the reader.</p>'
        '<p>CC0 applies only to the extent rights exist in project-created translation, typesetting, metadata, manifests, tools, and evidence. Original works, German editorial material, facsimiles, fonts, software, and other third-party material retain their own legal status and licenses.</p>'
    )
    return {
        "upload_type": "publication",
        "publication_type": "book",
        "title": "Эмми Нётер: полное русское издание корпуса / Emmy Noether: Complete Russian Corpus Edition",
        "creators": [{"name": "Noether, Emmy"}],
        "contributors": [{"name": "AI typesetting & translation", "type": "Other"}],
        "description": description,
        "access_right": "open",
        "license": "cc-zero",
        "publication_date": RELEASE_DATE,
        "version": VERSION,
        "keywords": [
            "Эмми Нётер", "Emmy Noether", "русский язык", "Russian", "перевод",
            "translation", "математика", "algebra", "machine-assisted edition",
        ],
        "related_identifiers": [
            {"identifier": GLOBAL_DOI, "relation": "isPartOf", "resource_type": "publication-other"},
            {"identifier": GERMAN_DOI, "relation": "isDerivedFrom", "resource_type": "publication-book"},
            {"identifier": REPOSITORY, "relation": "isSupplementedBy", "resource_type": "software"},
        ],
    }


def zip_exact(path: Path, entries: dict[str, bytes]) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(2026, 8, 22, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, entries[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(path, "r") as archive:
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {path}")
        names = archive.namelist()
        if names != sorted(entries):
            raise RuntimeError(f"ZIP entry order/inventory mismatch: {path}")
        for name, expected in entries.items():
            actual = archive.read(name)
            if actual != expected:
                raise RuntimeError(f"ZIP entry payload mismatch: {path}!{name}")
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "entries": len(entries),
        "uncompressed_bytes": sum(len(value) for value in entries.values()),
    }


def collect_decisions() -> tuple[dict[str, bytes], list[dict]]:
    entries: dict[str, bytes] = {}
    transformations: list[dict] = []
    for number in range(1, 18):
        stem = f"RU001-EDIT-{number:04d}"
        for suffix in (".json", ".md"):
            path = ROOT / "decision_records" / f"{stem}{suffix}"
            if path.is_file():
                relative = f"evidence/decisions/{path.name}"
                public, transformation = portable_public_text(relative, path.read_bytes())
                entries[relative] = public
                if transformation:
                    transformations.append(transformation)
    return entries, transformations


def collect_tools() -> dict[str, bytes]:
    entries = {
        f"tools/{name}": (ROOT / name).read_bytes()
        for name in PUBLIC_TOOL_NAMES
    }
    entries[f"tools/{Path(__file__).name}"] = Path(__file__).read_bytes()
    return entries


def historical_tool_hashes_tsv() -> bytes:
    lines = ["path\tbytes\tsha256\tpublic_disposition"]
    for name, (size, digest) in sorted(TOOL_PINS.items()):
        disposition = "portable_executable_in_archive" if name in PUBLIC_TOOL_NAMES else "canonical_source_hash_only_private_custody_paths_not_published"
        lines.append(f"{name}\t{size}\t{digest}\t{disposition}")
    return text_bytes("\n".join(lines) + "\n")


def assemble(output: Path, version_doi: str) -> dict:
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    output.mkdir(parents=True)
    release = output / "release"
    repository = output / "repository_tree"
    release.mkdir()
    repository.mkdir()

    portable_index = portable_machine_index(version_doi)
    portable_index_bytes = json_bytes(portable_index)
    readme_bytes = text_bytes(readme(version_doi))
    methodology_bytes = text_bytes(methodology())
    build_bytes = text_bytes(build_instructions())
    license_bytes = text_bytes(license_text())
    coverage_bytes = text_bytes(coverage_tsv())
    limitations_bytes = text_bytes(limitations_tsv())
    relations_bytes = json_bytes(datacite_relations(version_doi))
    zenodo_bytes = json_bytes(zenodo_metadata(version_doi))
    decision_entries, decision_transformations = collect_decisions()
    reference_index_public, reference_transformation = portable_public_text(
        "evidence/reference_sources/INDEX.json",
        (ROOT / "reference_sources/INDEX.json").read_bytes(),
    )
    public_transformations = list(decision_transformations)
    if reference_transformation:
        public_transformations.append(reference_transformation)
    transformations_bytes = json_bytes({
        "schema": "noether-public-copy-transformations/1.0",
        "policy": "Only public derivatives are path-sanitized; canonical controlled-workspace bytes and hashes remain unchanged.",
        "logical_roots": {
            "interlanguage-workspace://": "repository/project-relative custody root",
            "user-filesystem://": "non-workspace user-file root; resolve from the cited evidence record rather than a private path",
        },
        "files": sorted(public_transformations, key=lambda item: item["path"]),
    })
    tool_hashes_bytes = historical_tool_hashes_tsv()

    reader_source = ROOT / "release_v001_edit0017/pdf/emmy-noether-russian-v001-edit0017.pdf"
    reader_public = release / RELEASE_FILENAMES[0]
    shutil.copyfile(reader_source, reader_public)
    if reader_public.read_bytes() != reader_source.read_bytes():
        raise RuntimeError("reader copy mismatch")

    source_entries: dict[str, bytes] = {
        "README.md": readme_bytes,
        "BUILD.md": build_bytes,
        "LICENSE": license_bytes,
        "machine/LANGUAGE_EDITION_INDEX.json": portable_index_bytes,
        "machine/README.md": (ROOT / "machine_index/README.md").read_bytes(),
        "release_metadata/COMPONENT_COVERAGE.tsv": coverage_bytes,
        "release_metadata/DATACITE_RELATIONS.json": relations_bytes,
        "release_metadata/LIMITATIONS_AND_REVIEW.tsv": limitations_bytes,
        "release_metadata/RELEASE_IDENTITY.json": json_bytes({
            "schema": "noether-russian-release-identity/1.0",
            "version": VERSION,
            "publication_date": RELEASE_DATE,
            "concept_doi": CONCEPT_DOI,
            "version_doi": version_doi,
            "decision_head": "RU001-EDIT-0017",
            "repository": REPOSITORY,
        }),
        "source/base-papers1-43-ru.tex": (ROOT / "source/base-papers1-43-ru.tex").read_bytes(),
        "source/44-book-ru.tex": (ROOT / "source/44-book-ru.tex").read_bytes(),
        "source/45-ru.tex": (ROOT / "source/45-ru.tex").read_bytes(),
        "source/bib-ru.tex": (ROOT / "source/bib-ru.tex").read_bytes(),
        "assets/authority_rosette_native_supported_mask.png": (ROOT / "assets/authority_rosette_native_supported_mask.png").read_bytes(),
        "source/emmy-noether-russian-v001-edit0017.tex": (ROOT / "release_v001_edit0017/source/emmy-noether-russian-v001-edit0017.tex").read_bytes(),
        "build_ru_release_v001_edit0017.py": (ROOT / "build_ru_release_v001_edit0017.py").read_bytes(),
    }
    source_zip = release / RELEASE_FILENAMES[1]
    source_zip_record = zip_exact(source_zip, source_entries)

    evidence_entries: dict[str, bytes] = {
        "README.md": readme_bytes,
        "METHODOLOGY.md": methodology_bytes,
        "LICENSE": license_bytes,
        "COMPONENT_COVERAGE.tsv": coverage_bytes,
        "DATACITE_RELATIONS.json": relations_bytes,
        "LIMITATIONS_AND_REVIEW.tsv": limitations_bytes,
        "machine/LANGUAGE_EDITION_INDEX.json": portable_index_bytes,
        "machine/LANGUAGE_EDITION_INDEX.workspace.json": (ROOT / "machine_index/LANGUAGE_EDITION_INDEX.json").read_bytes(),
        "machine/README.md": (ROOT / "machine_index/README.md").read_bytes(),
        "evidence/RUSSIAN_DECISIONS_v001.jsonl": (ROOT / "RUSSIAN_DECISIONS_v001.jsonl").read_bytes(),
        "evidence/build-manifest.json": (ROOT / "release_v001_edit0017/evidence/build-manifest.json").read_bytes(),
        "evidence/RELEASE_AUDIT_VISUAL_QA_RU001_EDIT0017.json": (ROOT / "release_v001_edit0017/evidence/RELEASE_AUDIT_VISUAL_QA_RU001_EDIT0017.json").read_bytes(),
        "evidence/reference_sources/INDEX.json": reference_index_public,
        "evidence/reference_sources/README.md": (ROOT / "reference_sources/README.md").read_bytes(),
        "evidence/PUBLIC_COPY_TRANSFORMATIONS.json": transformations_bytes,
        "evidence/HISTORICAL_TOOL_SOURCE_HASHES.tsv": tool_hashes_bytes,
        "evidence/PREDECESSOR_RELEASE.json": json_bytes({
            "schema": "noether-russian-predecessor-release/1.0",
            "version": "2026.08.14-r1",
            "version_doi": "10.5281/zenodo.21926367",
            "concept_doi": CONCEPT_DOI,
            "preservation_note": "The predecessor remains immutable and publicly available; this successor records the complete RU001 decision lineage and does not silently rewrite the predecessor.",
        }),
    }
    evidence_entries.update(decision_entries)
    evidence_entries.update(collect_tools())
    evidence_zip = release / RELEASE_FILENAMES[2]
    evidence_zip_record = zip_exact(evidence_zip, evidence_entries)

    manifest_lines = []
    for name in RELEASE_FILENAMES[:3]:
        path = release / name
        manifest_lines.append(f"{sha256(path)}  {path.stat().st_size}  {name}")
    public_manifest = release / RELEASE_FILENAMES[3]
    write_exact(public_manifest, text_bytes("\n".join(manifest_lines) + "\n"))

    repo_files: dict[str, bytes] = {
        "README.md": readme_bytes,
        "METHODOLOGY.md": methodology_bytes,
        "BUILD.md": build_bytes,
        "LICENSE": license_bytes,
        "CITATION.cff": text_bytes(citation_cff(version_doi)),
        ".zenodo.json": zenodo_bytes,
        ".publication_identity.json": json_bytes({
            "schema": "emmy-noether-language-repository-identity/1.1",
            "language": "ru-Cyrl",
            "release_tag": f"v{VERSION}",
            "concept_doi": CONCEPT_DOI,
            "version_doi": version_doi,
            "repository": REPOSITORY,
            "decision_head": "RU001-EDIT-0017",
        }),
        f"reader/{RELEASE_FILENAMES[0]}": reader_public.read_bytes(),
        "source/base-papers1-43-ru.tex": source_entries["source/base-papers1-43-ru.tex"],
        "source/44-book-ru.tex": source_entries["source/44-book-ru.tex"],
        "source/45-ru.tex": source_entries["source/45-ru.tex"],
        "source/bib-ru.tex": source_entries["source/bib-ru.tex"],
        "source/emmy-noether-russian-v001-edit0017.tex": source_entries["source/emmy-noether-russian-v001-edit0017.tex"],
        "assets/authority_rosette_native_supported_mask.png": source_entries["assets/authority_rosette_native_supported_mask.png"],
        "machine/LANGUAGE_EDITION_INDEX.json": portable_index_bytes,
        "machine/README.md": source_entries["machine/README.md"],
        "evidence/RUSSIAN_DECISIONS_v001.jsonl": evidence_entries["evidence/RUSSIAN_DECISIONS_v001.jsonl"],
        "evidence/build-manifest.json": evidence_entries["evidence/build-manifest.json"],
        "evidence/RELEASE_AUDIT_VISUAL_QA_RU001_EDIT0017.json": evidence_entries["evidence/RELEASE_AUDIT_VISUAL_QA_RU001_EDIT0017.json"],
        "evidence/COMPONENT_COVERAGE.tsv": coverage_bytes,
        "evidence/DATACITE_RELATIONS.json": relations_bytes,
        "evidence/LIMITATIONS_AND_REVIEW.tsv": limitations_bytes,
        "evidence/PUBLIC_COPY_TRANSFORMATIONS.json": transformations_bytes,
        "evidence/HISTORICAL_TOOL_SOURCE_HASHES.tsv": tool_hashes_bytes,
        "evidence/PUBLIC_ARTIFACT_SHA256.tsv": text_bytes(
            "filename\tbytes\tsha256\n" + "".join(
                f"{name}\t{(release / name).stat().st_size}\t{sha256(release / name)}\n"
                for name in RELEASE_FILENAMES
            )
        ),
    }
    repo_files.update(decision_entries)
    repo_files.update(collect_tools())

    for relative, payload in sorted(repo_files.items()):
        write_exact(repository / relative, payload)
    tree_tsv = "path\tbytes\tsha256\n" + "".join(
        f"{relative}\t{len(payload)}\t{sha256_bytes(payload)}\n"
        for relative, payload in sorted(repo_files.items())
    )
    write_exact(repository / "evidence/REPOSITORY_TREE_SHA256.tsv", text_bytes(tree_tsv))

    package = {
        "schema": "noether-russian-public-contract/1.0",
        "release_id": "NOETHER-RU-v001-RU001-EDIT-0017",
        "version": VERSION,
        "publication_date": RELEASE_DATE,
        "concept_doi": CONCEPT_DOI,
        "version_doi": version_doi,
        "decision_head": "RU001-EDIT-0017",
        "authenticated_inputs": {
            relative: {"bytes": size, "sha256": digest}
            for relative, (size, digest) in sorted(PINNED_INPUTS.items())
        },
        "release_files": [record(release / name, output) for name in RELEASE_FILENAMES],
        "source_archive_verification": source_zip_record,
        "evidence_archive_verification": evidence_zip_record,
        "repository_files": [
            record(path, output)
            for path in sorted(repository.rglob("*"))
            if path.is_file()
        ],
        "public_status": {
            "editorial_holds": 0,
            "unresolved_editorial_dispositions": 0,
            "reader_pages": 609,
            "deterministic_build": "PASS",
            "finite_audit": "PASS",
            "visual_qa": "PASS",
            "native_review": "not completed; not claimed",
            "critical_edition": "not claimed",
        },
    }
    package_path = output / "PACKAGE_MANIFEST.json"
    write_exact(package_path, json_bytes(package))
    json.loads(package_path.read_text(encoding="utf-8"))
    return package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version-doi", required=True)
    args = parser.parse_args()
    if not args.version_doi.startswith("10.5281/zenodo."):
        parser.error("--version-doi must be a Zenodo DOI")
    authenticate_inputs()
    package = assemble(args.output.resolve(), args.version_doi)
    print(json.dumps({
        "status": "PASS",
        "version_doi": package["version_doi"],
        "release_files": package["release_files"],
        "repository_file_count": len(package["repository_files"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
