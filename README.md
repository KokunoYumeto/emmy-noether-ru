# Эмми Нётер — Математические труды на русском языке

Русский перевод собрания математических трудов Эмми Нётер (Emmy Noether, 1882–1935): статьи 1–43, лекции «Алгебра
гиперкомплексных величин» (зимний семестр 1929/30 года) в обработке М. Дойринга (M. Deuring), статья Г. Капферера
(H. Kapferer) с дополнением, написанным совместно с Э. Нётер, а также библиография и списки кратких сообщений,
рецензий и книг, в подготовке которых участвовала Эмми Нётер. Издание выходит в PDF и в редактируемом LaTeX.

[**Читать основной текст — PDF, 523 страницы**](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/01-noether-ru-base.pdf) ·
[Текст с редакционными исправлениями — PDF, 528 страниц](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/04-noether-ru-emendations.pdf) ·
[Все файлы издания от 27 октября 2026 года](https://github.com/KokunoYumeto/emmy-noether-ru/releases/tag/noether-ru-2026-11-15-r2)

## How this was made: AI's failure modes, and what we do about them

Everything here was produced by AI. The translation was made in a first pass mostly by GPT-5.6 Sol (OpenAI Codex,
reasoning effort ultra), by the user's account (July and August 2026). Its formulas were then brought into line with the German text, which Claude Opus 5.5 at
effort max compared page by page with Noether's printed originals (785 page checks, 26 October 2026), in automatic and
hand rounds by Claude Opus 5.5 at effort max (26-27 October; 2,570 lines in the last hand round), against the known
failures of AI translation of mathematics: renamed letters, formulas changed or dropped, statements narrowed, passages
reworked or garbled, sentences and displays dropped, broken layout. Every change passes a release filter, and every PDF
is checked for lines running into the margin (Claude Opus 5.5 at effort high, 15 November). No person has reviewed the
translation. What was done in each round, the measured figures and what is still open:
[How this was made](https://github.com/KokunoYumeto/emmy-noether#how-this-was-made-ais-failure-modes-and-what-we-do-about-them).

## Как создано издание

Русский текст переведён ИИ — моделями OpenAI Codex (по словам пользователя, в основном GPT-5.6 Sol с уровнем рассуждения ultra). Исправления и
набор выполнили OpenAI Codex — GPT-6 Astra, уровень рассуждения Ultra, 23–24 октября 2026 года, и Claude Opus 5.5
(Anthropic, уровень рассуждения max) 26–27 октября 2026 года; Claude Opus 5.5 сверил формулы с немецким текстом, прочитанным по печатным
страницам Нётер. Программу сборки создал OpenAI Codex — GPT-6 Astra, Ultra, 24 октября 2026 года.

## Состояние

Издание содержит все перечисленные труды, но статья 43 дана в сокращении (около трети полного текста), а статьи 41
и 42 — примерно в четырёх пятых объёма. Статьи 23, 24, 30, 31, 32, 34, 37 и 41–43, а также части статей 35 и 40
следуют более раннему английскому переводу, формулы которого местами расходятся с немецким текстом. В статье 2 три
сноски немецкого текста (примечание о Σ₃ и ссылки на Гордана — Кершенштейнера, с. 92 и 134) отмечены только
звёздочкой или присоединены к соседнему предложению. У PDF нет закладок. Перевод не проверялся человеком, и в нём
могут оставаться ошибки; кое-где формулы ещё могут следовать прежней немецкой транскрипции. Исправления принимаются
через [страницу issues](https://github.com/KokunoYumeto/emmy-noether-ru/issues).

## Содержание и с чего начать

Издание выходит в двух вариантах текста; у каждого есть PDF, один файл LaTeX и архив исходников:

| Вариант | PDF | LaTeX | Исходники |
|---|---|---|---|
| Основной текст: сохраняет чтения первых публикаций; редакционные примечания обсуждают эти чтения | [PDF, 523 с.](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/01-noether-ru-base.pdf) | [LaTeX](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/02-noether-ru-base.tex) | [ZIP](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/03-noether-ru-base-sources.zip) |
| Текст с редакционными исправлениями: исправления внесены в текст, каждое объяснено в редакционном примечании | [PDF, 528 с.](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/04-noether-ru-emendations.pdf) | [LaTeX](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/05-noether-ru-emendations.tex) | [ZIP](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/06-noether-ru-emendations-sources.zip) |

[Контрольные суммы SHA-256](https://github.com/KokunoYumeto/emmy-noether-ru/releases/download/noether-ru-2026-11-15-r2/07-noether-ru-SHA256SUMS.txt).
Те же файлы лежат в [`editions/2026-10-24-r2/ru/`](editions/2026-10-24-r2/ru/).

Сборка: файл LaTeX содержит все исходные файлы с их преамбулами. Программа Python
[`build.py`](editions/2026-10-24-r2/ru/build.py) извлекает их, компилирует с помощью XeLaTeX и соединяет PDF частей в
порядке чтения; нужны Python 3, pypdf, а также пакеты TeX и шрифты, указанные в преамбулах. Архив ZIP содержит те же
исходники в исходной структуре вместе с программой сборки.

Издание августа 2026 года (v2026.08.22-r2) хранится в [`reader/`](reader/) (PDF) и [`source/`](source/) (LaTeX);
методика его редакции описана в [METHODOLOGY.md](METHODOLOGY.md), сборка — в [BUILD.md](BUILD.md), записи проверок
лежат в [`evidence/`](evidence/). Немецкий текст, издания на других языках и известные различия между изданиями
перечислены на [центральной странице](https://kokunoyumeto.github.io/emmy-noether/).

## Авторы и источники

- Математические труды принадлежат Эмми Нётер и соавторам, названным в них: Вернер Шмейдлер (Werner Schmeidler,
  статья 17), Р. Брауэр (R. Brauer, статья 32), Р. Брауэр и Х. Хассе (H. Hasse, статья 38). Лекции 1929/30 года
  обработал М. Дойринг. Работа 45 принадлежит Г. Капфереру, дополнение к ней написано совместно с Э. Нётер. Сведения
  о первых публикациях, подписи и ссылки приводятся в текстах.
- Редакция августа 2026 года опиралась на немецкий проектный корпус NOETH-DE-ED-0015. Формулы нынешнего издания
  сверены с немецким текстом, сличённым постранично с первыми публикациями
  ([выпуск noether-de-2026-10-26](https://github.com/KokunoYumeto/modern-latex-manuscripts/releases/tag/noether-de-2026-10-26)).

## Права

Эмми Нётер умерла в 1935 году, поэтому её труды находятся в общественном достоянии в Европейском союзе и везде, где срок охраны истекает через 70 лет после смерти автора. В США её работы, впервые опубликованные в 1931 году или позднее, охраняются до истечения 95 лет после публикации (работы 1931 года становятся свободными 1 января 2027 года). В той мере, в какой издатель обладает правами на перевод, исправления и набор, выполненные ИИ, он передаёт их в общественное достояние по [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.ru). Лекции в записи M. Deuring, работа H. Kapferer и вклад названных соавторов этим заявлением не охватываются; права на них остаются за их авторами или наследниками.