# Методика русской редакции / Russian-edition methodology

## Русская версия

### 1. Что считается опорой

Редакционная опора этой линии — немецкий проектный корпус `NOETH-DE-ED-0015` (51A25101C04877AE740989E72B2AD65A7A7E65B081077C4A518BF1737AD5B907). Он служит контрольным объектом для структуры, формул и смысла, но не объявляется критическим немецким изданием. Русские версии являются переводными свидетелями этой редакции; они не превращаются в общий «канон русского математического языка».

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
