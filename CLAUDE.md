# Проект перевода Warhammer Fantasy Roleplay 4th Edition

## Текущая задача
Перевод книги **"Death on the Reik"** (Enemy Within Campaign, Volume 2) с английского на русский язык.
- Файл: `Enemy Within Campaign Volume 2 Death on the Reik.pdf`
- Страниц: 160
- Формат вывода: PDF с заменой текста (через PyMuPDF)

## Рабочий процесс

### Инструменты
- Python + PyMuPDF (`fitz`) — извлечение и замена текста в PDF
- Скрипты в папке `scripts/` (см. ниже)

### Этапы перевода
1. `scripts/extract.py` — извлекает текст постранично в `translations/death-on-the-reik/pageXXX_en.txt`
2. Перевести страницу, следуя инструкциям ниже → сохранить в `translations/death-on-the-reik/pageXXX_ru.txt`
3. **Обновить таблицу «Статус перевода»** в этом файле (CLAUDE.md) — добавить переведённые страницы со статусом ✅ и обновить строку «Последнее обновление»
4. `scripts/export_docx.py` — экспортирует билингвальный DOCX для проверки (**приоритет**)
5. `scripts/apply.py` — вставляет текст в PDF (по запросу, не обязательно после каждой партии)

### Формат файлов перевода
Каждый файл `pageXXX_ru.txt` — точное зеркало структуры оригинала:
- Блоки разделены пустой строкой
- Внутри блока — абзацы через `\n`
- Теги в начале строки определяют форматирование **всего блока**:

| Тег | Когда использовать |
|---|---|
| `[H1]` | Целый заголовок раздела первого уровня |
| `[H2]` | Целый подзаголовок второго уровня |
| `[B]` | Целый абзац, который в оригинале полностью жирный (например, отдельная строка-название книги, стоящая как самостоятельный блок) |
| `[I]` | Целый абзац, который в оригинале полностью курсивный |
| _(без тега)_ | Обычный абзац — **даже если внутри есть отдельные жирные или курсивные слова** |

⚠️ **Важно:** `[B]` и `[I]` — это теги **абзаца**, а не инлайн-разметка. Если жирное/курсивное выделение встречается только внутри обычного предложения — писать блок без тега, как обычный текст. Не нужно дробить предложение на части ради жирного слова.

- Счётчик блоков должен строго совпадать с EN-файлом — блоки не объединять и не дробить
- Не переведённые элементы (таблицы, колонтитулы) оставляются as-is

---

## Правила перевода

### Стиль перевода
> Ты профессиональный переводчик. Переводи на русский язык литературной нормы: избегай кальки с английского, используй живые русские конструкции. Не переводи дословно — передавай смысл. Избегай канцеляризмов и слов-паразитов вроде «данный», «осуществить», «является».

- Тон: **литературный, атмосферный** — это художественный текст с игровыми правилами.
- Флафф (художественные описания): живой язык, допустимы литературные обороты.
- Правила механики: точный, однозначный язык; один термин = одно значение.
- Обращение к ведущему: «ведущий» (не «Мастер», не «вы») — **подтверждено из существующих переводов**.
- Обращение к игрокам: «персонажи» (не «герои», не «adventurers», не «авантюристы»).
- Избегать слов-сорняков: **данный, осуществить, является, в рамках, посредством, в целях**.
- Избегать калек: «адвентурер» → «персонаж», «квест» → «задание/поручение», «мастер» → «ведущий».
- Перед финальным сохранением перевода — проверить через `check_text` (MCP LanguageTool).

### Сохранение форматирования оригинала
⚠️ **Форматирование оригинала ОБЯЗАТЕЛЬНО сохранять:**
- Если в оригинале **заголовок** → использовать `[H1]` или `[H2]`
- Если в оригинале **жирный шрифт** → использовать `[B]`
- Если в оригинале *курсив* → использовать `[I]`
- Имена собственных персонажей и топонимы внутри обычного текста оставлять как есть (они не выделяются отдельным тегом, если в оригинале не выделены)
- Счётчик блоков должен строго совпадать с EN-файлом — не объединять и не дробить блоки

### Приоритет терминологии

⚠️ **МАКСИМАЛЬНЫЙ ПРИОРИТЕТ: Глоссарий.** При переводе любого термина, имени, топонима — **первым делом искать в глоссарии**. Только при отсутствии в глоссарии допустимо придумывать перевод самостоятельно.

Строгий порядок:

1. **Глоссарий — колонка «Студия 101»** (`RU_101`) — если есть, использовать **обязательно**.
2. **Глоссарий — колонка «Мы»** (`RU_WE`) — если перевода 101 нет, но есть наш вариант.
3. **Спросить пользователя** — если термин отсутствует в обоих столбцах.

Полный структурированный глоссарий (13 719 записей, UTF-8):
`C:/Users/user/Desktop/ВФРП/glossary_structured.txt`
Формат: `EN | RU_101 | RU_WE | COMMENT`, разбит по разделам.

Оригинальный файл: `C:/Users/user/Desktop/ВФРП/Глоссарий.xlsx` (листы: «Игровая терминология», «ИменаНазвания»)

### Что НЕ переводить
- Имена персонажей — транслитерировать кириллицей по глоссарию (лист «ИменаНазвания»)
- `Magister Impedimentae`, `Ordo Septenarius` — не переводить, оставить латиницей
- Аббревиатуры характеристик в тексте писать по-русски: ББ, ДБ, С, В, И, Пр, Л, Инт, СВ, Х
- Колонтитулы книги (WARHAMMER FANTASY ROLEPLAY) и номера страниц — не трогать
- Копирайт и издательские уведомления — не трогать

### Имена мест
Топонимы — по глоссарию (лист «ИменаНазвания»). Если нет — транслитерировать по немецкому произношению.

---

## Глоссарий терминов

> Источник: `Глоссарий.xlsx`. Studio 101 имеет приоритет над "Мы".

### Характеристики (Characteristics)
⚠️ Аббревиатуры **подтверждены** из реальных переводов (Враг в тени, Смерть на Рейке доп. материалы).

| EN | RU (полное) | Сокр. в стат-блоке |
|---|---|---|
| Movement | Скорость | Ск |
| Weapon Skill | Ближний бой | ББ |
| Ballistic Skill | Дальний бой | ДБ |
| Strength | Сила | С |
| Toughness | Выносливость | В |
| Initiative | Инициатива | И |
| Agility | Проворство | Пр |
| Dexterity | Ловкость рук | Л |
| Intelligence | Интеллект | Инт |
| Willpower | Сила Воли | СВ |
| Fellowship | Харизма | Х |
| Wounds | Здоровье | Зд |

Формат стат-блока НИП (пример):
```
Ск ББ ДБ С В И Пр Л Инт СВ Х Зд
4  35 38 28 29 45 33 36  51 45 51 10
```

### Ресурсы персонажа
| EN | RU |
|---|---|
| Wounds | Здоровье (в стат-блоке: Зд) |
| Fate | Судьба |
| Fortune | Удача |
| Resilience | Упорство |
| Resolve | Решимость |
| Motivation | Мотивация |
| Corruption | Осквернение |
| Mutation | Мутация |
| Experience Points (XP) | Очки опыта (ОО) |

### Игровые механики
| EN | RU |
|---|---|
| Career | Профессия |
| Career Path | Карьерный путь |
| Class | Класс |
| Advance | Улучшение |
| Characteristic Advance | Улучшение характеристики |
| Skill | Навык |
| Talent | Талант |
| Trapping | Имущество |
| Test | Проверка |
| SL (Success Level) | УУ (Уровень успеха) |
| Difficulty | Сложность |
| Advantage | Преимущество |
| Condition | Состояние |
| Critical Wound | Травма |
| Engaged | Участие в ближнем бою |

### Таланты (Talents)
| EN | RU (Studio 101) |
|---|---|
| Accurate Shot | Точный выстрел |
| Acute Sense | Обостренное восприятие |
| Aethyric Attunement | Эфирный унисон |
| Alley Cat | Бродячий кот |
| Ambidextrous | Амбидекстр |
| Animal Affinity | Сродство с животными |
| Arcane Magic (Lore) | Школа магии |
| Argumentative | Спорщик |
| Artistic | Искусник |
| Attractive | Привлекательность |
| Battle Rage | Боевая ярость |
| Beat Blade | Батман |
| Beneath Notice | Простолюдин |
| Berserk Charge | Яростный натиск |
| Blather | Трёп |
| Bless (Divine Lore) | Благословение |
| Bookish | Книжный червь |
| Break and Enter | Взлом с проникновением |
| Briber | Взяткодатель |
| Cardsharp | Картежник |
| Careful Strike | Выверенное попадание |
| Carouser | Заядлый кутила |
| Catfall | Кошачья легкость |
| Cat-tongued | Витийство |
| Chaos Magic | Магия Хаоса |
| Combat Aware | Бдительность |
| Combat Master | Бывалый воин |
| Combat Reflexes | Быстрая реакция |
| Commanding Presence | Аура величия |
| Concoct | Походный рецепт |
| Contortionist | Гуттаперчевость |
| Coolheaded | Самообладание |
| Crack the Whip | Щелчок кнутом |
| Craftsman (Trade) | Умелец (Ремесло) |
| Criminal | Преступник |
| Deadeye Shot | Меткий выстрел |
| Dealmaker | Коммерсант |
| Detect Artefact | Распознание артефакта |
| Diceman | Игрок в кости |
| Dirty Fighting | Грязные приемы |
| Disarm | Разоружение |
| Distract | Отвлекающий манёвр |
| Doomed | Роковое пророчество |
| Drilled | Строевая подготовка |
| Dual Wielder | Двойная атака |
| Embezzle | Расхититель |
| Enclosed Fighter | Тесный контакт |
| Etiquette (Social Group) | Этикет (Социальная группа) |
| Fast Hands | Быстрые руки |
| Fast Shot | Быстрый выстрел |
| Fearless | Бесстрашие |
| Feint | Финт |
| Field Dressing | Полевая перевязка |
| Fisherman | Рыбак |
| Flagellant | Флагеллант |
| Flee! | Поспешное бегство |
| Fleet Footed | Быстрые ноги |
| Frenzy | Ярость |
| Frightening | Устрашающий вид |
| Furious Assault | Свирепый натиск |
| Gregarious | Общительность |
| Gunner | Стрелковая Подготовка |
| Hardy | Здоровяк |
| Hatred (Group) | Ненависть |
| Holy Hatred | Праведный гнев |
| Holy Visions | Видения свыше |
| Hunter's Eye | Охотничье чутьё |
| Impassioned Zeal | Страстное рвение |
| Implacable | Суровый |
| In-fighter | Полный контакт |
| Inspiring | Воодушевление |
| Instinctive Diction | Безупречная дикция |
| Invoke | Божественное вмешательство |
| Iron Jaw | Стальная челюсть |
| Iron Will | Железная воля |
| Jump Up | Подскок |
| Kingpin | Большая шишка |
| Lightning Reflexes | Молниеносная реакция |
| Linguistics | Полиглот |
| Lip Reading | Чтение по губам |
| Luck | Фортуна |
| Magical Sense | Магическое чутьё |
| Magic Resistance | Устойчивость к магии |
| Magnum Opus | Magnum Opus |
| Marksman | Меткость |
| Master of Disguise | Мастер перевоплощения |
| Master Orator | Ритор |
| Master Tradesman | Мастер своего дела |
| Menacing | Грозный вид |
| Mimic | Имитатор |
| Night Vision | Сумеречное зрение |
| Nimble Fingered | Ловкие пальцы |
| Noble Blood | Благородная кровь |
| Nose for Trouble | Чутьё на неприятности |
| Numismatics | Нумизмат |
| Old Salt | Морской волк |
| Orientation | Чувство направления |
| Panhandle | Жалобный вид |
| Perfect Pitch | Абсолютный слух |
| Petty Magic | Простейшая магия |
| Pharmacist | Фармацевт |
| Pilot | Рулевой |
| Public Speaker | Оратор |
| Pure Soul | Духовная чистота |
| Rapid Reload | Быстрая перезарядка |
| Reaction Strike | Упреждающий удар |
| Read/Write | Грамотность |
| Relentless | Непреклонность |
| Resistance | Устойчивость |
| Resolute | Целеустремленность |
| Reversal | Рокировка |
| Riposte | Рипост |
| River Guide | Знаток рек |
| Robust | Живучесть |
| Roughrider | Выездка |
| Rover | Скиталец |
| Savant | Кладезь знаний |
| Savvy | Смекалка |
| Scale Sheer Surface | Цепкость |
| Schemer | Интриган |
| Sea Legs | Мореплаватель |
| Seasoned Traveller | Бывалый путешественник |
| Second Sight | Второе зрение |
| Secret Identity | Альтер эго |
| Shadow | Тень |
| Sharp | Проницательность |
| Sharpshooter | Отличный стрелок |
| Shieldsman | Щитоносец |
| Sixth Sense | Шестое чувство |
| Slayer | Убийца чудовищ |
| Small | Небольшой |
| Sniper | Снайпер |
| Speedreader | Скорочтение |
| Sprinter | Бегун |
| Step Aside | Разрыв дистанции |
| Stone Soup | Каменный суп |
| Stout-hearted | Отважное сердце |
| Strider | Ходок |
| Strike Mighty Blow | Могучий удар |
| Strike to Injure | Безжалостный удар |
| Strike to Stun | Ошеломляющий удар |
| Strong Back | Сильная спина |
| Strong Legs | Сильные ноги |
| Strong-minded | Твердость духа |
| Strong Swimmer | Отличный пловец |
| Sturdy | Бугай |
| Suave | Учтивость |
| Super Numerate | Счетовод |
| Supportive | Услужливость |
| Sure Shot | Верный выстрел |
| Surgery | Хирург |
| Tenacious | Упрямство |
| Tinker | Мастер на все руки |
| Tower of Memories | Башня памяти |
| Trapper | Ловчий |
| Trick Riding | Лихой наездник |
| Tunnel Rat | Тоннельная крыса |
| Unshakeable | Стреляный боец |
| Very Resilient | Закалка |
| Very Strong | Силач |
| Warleader | Командир |
| War Wizard | Боевой маг |
| Warrior Born | Прирожденный воин |
| Waterman | Речной волк |
| Wealthy | Богач |
| Well-prepared | Запасливость |
| Witch! | Ведьма |
| Suffuse with Ulgu | Единение с Улгу |

### СКИЛЛЫ (Skills)
| EN | RU (Studio 101) |
|---|---|
| Animal Care | Обращение с животными |
| Animal Training | Дрессировка |
| Art | Искусство |
| Athletics | Атлетика |
| Bribery | Подкуп |
| Channelling | Концентрация |
| Charm | Обаяние |
| Charm Animal | Усмирение Животных |
| Climb | Лазание |
| Consume Alcohol | Кутёж |
| Cool | Хладнокровие |
| Dodge | Уклонение |
| Drive | Вождение |
| Endurance | Стойкость |
| Entertain | Артистизм |
| Evaluate | Оценка |
| Gamble | Азартные игры |
| Gossip | Сплетничество |
| Haggle | Торговля |
| Heal | Лечение |
| Intimidate | Запугивание |
| Intuition | Интуиция |
| Language | Язык |
| Leadership | Лидерство |
| Lore | Знание |
| Melee | Рукопашный бой |
| Navigation | Ориентирование |
| Outdoor Survival | Выживание |
| Perception | Наблюдательность |
| Perform | Сценическое искусство |
| Pick Lock | Взлом |
| Play | Музицирование |
| Pray | Молитвословие |
| Ranged | Стрельба |
| Research | Книжные изыскания |
| Ride | Верховая езда |
| Row | Гребля |
| Sail | Хождение под парусом |
| Secret Signs | Тайные знаки |
| Set Trap | Обращение с ловушками |
| Sleight of Hand | Ловкость рук |
| Stealth | Скрытность |
| Swim | Плавание |
| Track | Выслеживание |
| Trade | Ремесло |

### ЧЕРТЫ СУЩЕСТВ (Creature Traits)
| EN | RU (Studio 101) |
|---|---|
| Afraid | Боязнь (объект) |
| Amphibious | Амфибия |
| Animosity | Враждебность (к группе) |
| Arboreal | Лесной житель |
| Armour | Броня (класс) |
| Belligerent | Воинственность |
| Bestial | Зверь |
| Big | Крупный |
| Bite | Укус + урон |
| Blessed | Благословение (божество) |
| Bounce | Прыгучесть |
| Breath | Смертоносное дыхание + урон (тип) |
| Brute | Верзила |
| Champion | Воитель |
| Chill Grasp | Леденящее касание |
| Clever | Острый ум |
| Cold-Blooded | Холодная кровь |
| Constrictor | Душитель |
| Construct | Искусственное создание |
| Corrosive Blood | Едкий ихор |
| Corruption | Источник скверны (сила) |
| Cunning | Хитрость |
| Daemonic | Демон (порог) |
| Dark Vision | Ночное зрение |
| Die Hard | Крепкий орешек |
| Distracting | Дезориентация |
| Disease | Разносчик (болезнь) |
| Elite | Опытный боец |
| Ethereal | Бестелесность |
| Fast | Быстрый |
| Fear | Аура страха (уровень) |
| Flight | Полёт (скорость) |
| Frenzy | Ярость |
| Fury | Свирепость |
| Ghostly Howl | Призрачный вой |
| Hardy | Здоровяк |
| Hatred | Ненависть (к группе) |
| Horns | Рога (вид) + урон |
| Hungry | Голод |
| Immunity | Невосприимчивость (тип урона) |
| Immunity to Psychology | Невозмутимость |
| Infected | Заразный |
| Infestation | Паразиты |
| Leader | Лидер |
| Magic Resistance | Устойчивость к магии (показатель) |
| Magical | Магическая атака |
| Mental Corruption | Ментальная порча |
| Miracles | Чудотворец (божество) |
| Mutation | Мутация |
| Night Vision | Сумеречное зрение |
| Painless | Невосприимчивость к боли |
| Petrifying Gaze | Окаменяющий взгляд |
| Prejudice | Предубеждение (к группе) |
| Ranged | Стрельба + урон (дальнобойность) |
| Rear | Сокрушительная поступь |
| Regenerate | Регенерация |
| Size | Размер (категория) |
| Skittish | Пугливость |
| Spellcaster | Магический дар (Школа) |
| Stealthy | Незаметность |
| Stride | Широкий шаг |
| Stupid | Безмозглый |
| Swamp-strider | Болотный житель |
| Swarm | Скопище |
| Tail Attack | Удар хвостом + урон |
| Tentacles | # щупалец + урон |
| Territorial | Территориальный |
| Terror | Аура ужаса (уровень) |
| Tongue Attack | Атака языком + урон (дальность) |
| Tough | Закалённый |
| Tracker | Следопыт |
| Trained (Broken) | Приручённый |
| Trained (Drive) | Тяговой |
| Trained (Guard) | Сторожевой |
| Trained (Mount) | Верховой |
| Trained (War) | Боевой |
| Undead | Нежить |
| Unstable | Нестабильность |
| Vampiric | Вампир |
| Venom | Яд (модификатор) |
| Vomit | Отрыжка |
| Wallcrawler | Верхолаз |
| Ward | Оберег (порог) |
| Weapon | Оружие + урон |
| Web | Паутина (сила) |

### БОЛЕЗНИ И СИМПТОМЫ
| EN | RU (Studio 101) |
|---|---|
| Galloping Trots | Бешеная золотуха |
| Bloody Flux | Кровавый понос |
| Blood Rot | Кровяная гниль |
| Ratte Fever | Крысиная лихорадка |
| Minor Infection | Лёгкая инфекция |
| Festering Wound | Нагноение |
| Packer's Pox | Скорняжная оспа |
| Itching Pox | Сыпучая чесотка |
| Black Plague | Чёрная чума |
| Buboes | Бубоны |
| Gangrene | Гангрена |
| Fever | Жар |
| Blight | Летальный исход |
| Wounded | Незаживающая рана |
| Lingering | Осложнения |
| Flux | Понос |
| Malaise | Слабость |
| Convulsions | Судороги |
| Pox | Сыпь |
| Nausea | Тошнота |
| Coughs and Sneezes | Чихание и кашель |

### СОСТОЯНИЯ (Conditions)
| EN | RU (Studio 101) |
|---|---|
| Ablaze | Охвачен огнём |
| Bleeding | Истекает кровью / кровотечение |
| Blinded | Ослеплён |
| Broken | В панике |
| Deafened | Оглушён |
| Entangled | Обездвижен |
| Fatigued | Устал |
| Poisoned | Отравлен |
| Prone | Сбит с ног |
| Stunned | Ошеломлён |
| Surprised | Застигнут врасплох |
| Unconscious | Без сознания |

### ЗАКЛИНАНИЯ (первые 150 записей)
| EN | RU (Studio 101) |
|---|---|
| Acquiescence | Горестное принятие |
| Aethyric Armour | Эфирный доспех |
| Aethyric Arms | Эфирное оружие |
| Amber Talons | Янтарные когти |
| An Invitation | Приглашение |
| Anchorite's Endurance | Стойкость отшельника |
| Animal Friend | Друг животных |
| Animal Instincts | Звериные инстинкты |
| Aqshy's Aegis | Эгида Акши |
| Arrow Shield | Защита от стрел |
| As Verena Is My Witness | Да будет Верена мне свидетельницей |
| Balm to a Wounded Mind | Бальзам для израненной души |
| Banishment | Изгнание |
| Barkskin | Деревянная шкура |
| Beacon of Righteous Virtue | Светоч праведной добродетели |
| Bearings | Магический компас |
| Beast Form | Облик зверя |
| Beast Master | Владыка зверей |
| Beast Tongue | Язык зверей |
| Becalm | Штиль |
| Bitter Catharsis | Болезненное очищение |
| Blast | Взрыв |
| Blazing Sun | Слепящее солнце |
| Blessing of Battle | Благословение битвы |
| Blessing of Breath | Благословение дыхания |
| Blessing of Charisma | Благословение притягательности |
| Blessing of Conscience | Благословение совести |
| Blessing of Courage | Благословение отваги |
| Blessing of Finesse | Благословение грации |
| Blessing of Fortune | Благословение везения |
| Blessing of Grace | Благословение стремительности |
| Blessing of Hardiness | Благословение крепости |
| Blessing of Healing | Благословение исцеления |
| Blessing of Might | Благословение мощи |
| Blessing of Protection | Благословение защиты |
| Blessing of Recuperation | Благословение выздоровления |
| Blessing of Righteousness | Благословение праведности |
| Blessing of Savagery | Благословение свирепости |
| Blessing of Tenacity | Благословение живучести |
| Blessing of The Hunt | Благословение охоты |
| Blessing of Wisdom | Благословение мудрости |
| Blessing of Wit | Благословение сметливости |
| Blight | Порча |
| Blind Justice | Слепое правосудие |
| Blinding Light | Слепящий свет |
| Bolt | Стрела |
| Breath | Смертоносное дыхание |
| Bridge | Мост |
| Careful Step | Лёгкая поступь |
| Caress of Laniph | Ласка Ланиф |
| Cat's Eyes | Кошачий глаз |
| Cauterise | Прижигание |
| Cerulean Shield | Лазурный щит |
| Chain Attack | Цепной разряд |
| Choking Shadows | Удушающие тени |
| Clarity of Thought | Ясность мыслей |
| Comet of Casandora | Комета Касандоры |
| Conserve | Консервация |
| Corrosive Blood | Едкий ихор |
| Creeping Menace | Ползучая напасть |
| Crown of Flame | Огненный венец |
| Crucible of Chamon | Горн Шамона |
| Curse of Crippling Pain | Проклятие нестерпимой боли |
| Curse of Ill-Fortune | Проклятие неудачи |
| Daemonbane | Бич демонов |
| Dark Vision | Ночное зрение |
| Dart | Дротик |
| Dazzle | Вспышки |
| Death Mask | Маска смерти |
| Destroy Lesser Daemon | Уничтожение низшего демона |
| Destroy Undead | Уничтожение нежити |
| Detect Daemon | Обнаружение демона |
| Distracting | Дезориентация |
| Dome | Купол |
| Dooming | Обречение |
| Doppelganger | Доппельгангер |
| Drain | Испивание |
| Drop | Дырявые руки |
| Drowned Man's Face | Лицо утопленника |
| Dying Words | Посмертные слова |
| Eagle's Eye | Орлиный взор |
| Earthblood | Кровь земли |
| Earthpool | Земляная купель |
| Eavesdrop | Подслушивание |
| Enchant Weapon | Зачарование оружия |
| Entangle | Обездвижение |
| Fair Winds | Попутный ветер |
| Fat of the Land | Жир земли |
| Fate's Fickle Fingers | Ветреная удача |
| Fearsome | Устрашающий облик |
| Feather of Lead | Свинцовое перо |
| Firewall | Огненная стена |
| Flaming Hearts | Пылкие сердца |
| Flaming Sword of Rhuin | Пылающий меч Рюина |
| Flight | Полёт |
| Flock of Doom | Смертоносная стая |
| Fool's Gold | Золото дурака |
| Forest of Thorns | Лес шипов |
| Forge of Chamon | Кузница Шамона |
| Fury's Call | Зов фурии |
| Glittering Robe | Блистающая мантия |
| Goodwill | Добрая воля |
| Great Fires of U'Zhul | Великое пламя У'Зула |
| Gust | Порыв ветра |
| Haunting Horror | Проклятое место |
| Healing Light | Целительный свет |
| Heed Not the Witch | Не внемли ведьмовским речам |
| Hoarfrost's Chill | Леденящий страх |
| Howl of the Wolf | Волчий вой |
| Hunter's Hide | Шкура охотника |
| Illusion | Иллюзия |
| Inspiring | Боевое рвение |
| King of the Wild | Царь дикой природы |
| Last Rites | Отходная молитва |
| Leaping Stag | Прыткость оленя |
| Lie of the Land | Лик земли |
| Lifebloom | Цветение жизни |
| Light | Свет |
| Lord of the Hunt | Владыка охоты |
| Magic Flame | Магический огонёк |
| Magic Shield | Магический щит |
| Manann's Bounty | Щедрость Мананна |
| Manifest Lesser Daemon | Призыв низшего демона |
| Marsh Lights | Магические светляки |
| Martyr | Мученик |
| Mindslip | Ускользающие воспоминания |
| Mirkride | Взгляд сквозь Межу |
| Move Object | Телекинез |
| Mundane Aura | Обыденная аура |
| Murmured Whisper | Чревовещание |
| Mutable Metal | Податливый металл |
| Mystifying Miasma | Мистический туман |
| Nepenthe | Снадобье забвения |
| Net of Amyntok | Сеть Аминтока |
| Nostrum | Панацея |
| Octagram | Октаграмма |
| Open Lock | Магическая отмычка |
| Part the Branches | Сумеречная прогулка |
| Pelt of the Winter Wolf | Шкура зимнего волка |

### Места и названия (из ИменаНазвания)

#### Важные для Death on the Reik
| Оригинал | RU (Studio 101) | RU (Мы) |
|---|---|---|
| Wittgenstein | - | Виттгенштайн |
| Ludwig von Wittgenstein | - | Людвиг фон Витгенштайн |
| Kemperbad | Кемпербад | Кемпербад |
| Weissbruck | Вайсбрюк | - |
| Grissenwald | - | Гриссенвальд |
| The Old World | Старый Свет | Старый Свет |
| The Empire | Империя | Империя |
| The Reik | - | Рейк (река) |
| Reikland | - | Рейкланд |
| Altdorf | - | Альтдорф |
| Bögenhafen | - | Богенхафен |

#### Империя: правители и провинции
| Оригинал | RU (Studio 101) | RU (Мы) |
|---|---|---|
| Emperor Karl-Franz I | Император Карл-Франц I из Дома Хользвиг-Шлиштайнов... | - |
| Grand Provinces | Великие провинции | Великие провинции |
| Elector Count(ess) | курфюрст/курфюрстина | курфюрст/курфюрстина |
| Runefang | Рунный клык | Рунный клык |
| Reikland Diet | Рейкстаг | Рейкстаг |
| Freistadt | вольный город | вольный город |
| Burgomeister | бургомистр | бургомистр |

#### Сложности проверок
| EN | RU (Studio 101) |
|---|---|
| Very Easy (+60) | Элементарная (+60) |
| Easy (+40) | Лёгкая (+40) |
| Average (+20) | Заурядная (+20) |
| Challenging (+0) | Серьёзная (+0) |
| Difficult (-10) | Трудная (-10) |
| Hard (-20) | Тяжёлая (-20) |

### Боевые термины
| EN | RU |
|---|---|
| Armour (AP / КБ) | Броня |
| Armour Points | Класс брони (КБ) |
| Encumbrance / Weight | Вес |
| Reach | Досягаемость |
| Damage | Урон |
| Ranged Attack | Дальняя атака |
| Reload | Перезарядка |
| Charging | Атака с разгона |
| Engaged | Участие в ближнем бою |
| Point Blank | Ближняя дистанция |
| Short Range | Короткая дистанция |
| Long Range | Дальняя дистанция |
| Extreme Range | Предельная дистанция |

### Магия
| EN | RU |
|---|---|
| Spell | Заклинание |
| Casting Number (CN) | Сложность заклинания (КН) |
| Channelling | Концентрация |
| Winds of Magic | Ветра Магии |
| Petty Magic | Простейшая магия |
| Arcane Magic | Школа магии (Studio 101) / Тайная магия |
| Divine Magic | Божественная магия |
| Prayer | Молитва |
| Miracle | Чудо |
| Blessing | Благословение |
| Witchcraft | Ведьмовство |
| Hedgecraft | Знахарство |
| Daemonology | Демонология |
| Necromancy | Некромантия |

### Снаряжение и оружие
| EN | RU |
|---|---|
| Gold Crown (GC) / КР | Золотая крона (КР) |
| Silver Shilling (SS) | Шиллинг |
| Brass Penny (BP) / п | Медная пенни (п) |
| Availability | Доступность |
| Common | Распространённое |
| Scarce | Редкое |
| Rare | Раритет |
| Exotic | Экзотическое |
| Trappings / Imushchestvo | Имущество |
| Leather Jack | Кожаная куртка |
| Mail Shirt / Mail Coat | Кольчуга |
| Sword | Меч |
| Dagger | Кинжал |
| Hand Axe | Ручной топор |
| Crossbow | Арбалет |
| Pistol | Пистолет |
| Blunderbuss | Мушкетон |
| Shield | Щит |

### Расы / Народы
| EN | RU |
|---|---|
| Human | Человек |
| Dwarf | Гном |
| Halfling | Хафлинг |
| High Elf | Высший Эльф |
| Wood Elf | Лесной Эльф |
| Goblin | Гоблин |
| Orc | Орк |
| Skaven | Скавен |
| Beastman / Beastmen | Зверолюд / Зверолюды |

### Религия и культы
| EN | RU |
|---|---|
| Sigmar | Сигмар |
| Ulric | Ульрик |
| Ranald | Ранальд |
| Shallya | Шалья |
| Morr | Морр |
| Taal | Тааль |
| Rhya | Рия |
| Manann | Манан |
| Verena | Верена |
| Myrmidia | Мирмидия |
| Witch Hunter | Охотник на ведьм |
| Priest | Жрец |
| High Priest | Верховный жрец |
| Initiate | Диакон (карьера) |

### Силы Хаоса
| EN | RU |
|---|---|
| Chaos | Хаос |
| Warpstone | Варп-камень |
| Ruinous Powers | Губительные Силы |
| Tzeentch | Тзинч |
| Khorne | Кхорн |
| Nurgle | Нургл |
| Slaanesh | Слаанеш |
| Purple Hand | Пурпурная Длань |
| Red Crown | Красная Корона |
| Cultist | Культист |
| Daemon | Демон |
| Mutant | Мутант |

### Социальные термины и организации
| EN | RU |
|---|---|
| Game Master (GM) | Ведущий |
| Player Character (PC) | Игровой персонаж (ИП) |
| Non-Player Character (NPC) | Неигровой персонаж (НИП) |
| Adventurer | Авантюрист |
| Party | Группа |
| River Warden / Riverwarden | Речной стражник |
| River Recruit | Новобранец речной стражи |
| Shipsword | Корабельный меч (карьера) |
| Barge Master | Капитан баржи |
| Boatman | Лодочник |
| Watchman | Городской стражник |
| Apothecary | Аптекарь |
| Master Apothecary | Мастер-аптекарь |
| Scholar | Учёный |
| Wizard | Маг |
| Master Wizard | Магистр |
| Wizard's Apprentice | Ученик мага |
| Witch Hunter | Охотник на ведьм |
| Bounty Hunter | Охотник за головами |
| Road Warden | Дорожный стражник |
| Engineer | Инженер |
| Master Engineer | Мастер-инженер |

### Термины и персонажи Death on the Reik
⚠️ Термины **подтверждены** из «Смерть на Рейке: дополнительные материалы (v1-0)» и глоссария.

#### Общие термины кампании
| EN | RU |
|---|---|
| Enemy Within (кампания) | Враг Внутри |
| Death on the Reik | Смерть на Рейке |
| Magister Impedimentae | Magister Impedimentae (не переводить) |
| Ordo Septenarius | Ordo Septenarius (не переводить) |
| Purple Hand | Пурпурная Длань |
| Red Crown | Красная Корона |
| Wittgenstein (family/castle) | Виттгенштайн |
| warpstone | варп-камень |
| meteorite / chunk of Morrslieb | обломок варп-камня / осколок Моррслиба |
| inheritance | наследство |
| River Warden / River Guard | Имперская речная стража |
| lock (шлюз) | шлюз |
| toll | пошлина |
| barge | баржа |
| NPC sidebars | «Персонажи ведущего» |
| Adventure Seed | Зацепка приключения |
| Grognard Box | Врезка Гроньяра |
| Casting a Shadow | Отброшенная тень |
| Success Levels (SL) | Уровень успеха (УУ) |
| Availability: Common/Rare/Scarce/Exotic | Распространённый / Редкий / Раритетный / Экзотический |

#### Персонажи
| EN | RU |
|---|---|
| Kastor Lieberung | Кастор Либерунг |
| Etelka Herzen | Этелька Херцен (волшебница из Чёрных Пиков близ Гриссенвальда) |
| Elvyra Kleinestun | Эльвира Кляйнестун (аптекарь из Вайсбрюка) |
| Josef Quartjin | Йозеф Квартджин (хозяин баржи «Берибели») |

#### Скавены (из глоссария)
| EN | RU |
|---|---|
| SKAVENSLAVE | Скавены-рабы |
| CLANRAT | Крысородичи |
| STORMVERMIN | Штурмовые грызни |
| Rat Ogres | Крысоогры |
| CLANRAT CLAWLEADER | Крысородич когтевод |
| STORMVERMIN FANGLEADER | Штурмовой грызень грызовод |
| CHIEFTAIN | Вожак |
| WARLOCK-ENGINEER | Инженер-колдун |
| Grey Seers | Серые провидцы |
| Seerlord | Верховный провидец |
| Farsqueaker | Пискозвяк |
| Skaven musk | Скавенский мускус |
| Warptokens | Варп-жетон |
| LORE OF RUIN | Разрушение (школа магии скавенов) |
| Warp Lightning | Варп-молния |
| Warpfire Thrower | Огнемёт варп-огня |
| Poisoned Wind Globe | Шар ядовитого ветра |
| Warplock Jezzail | Варпзамковый джезайл |
| Ratling Gun | Пушка крыслинга |
| Doomwheel | Колесо рока |
| Screaming Bell | Вопящий колокол |
| PURPLE HAND CULTIST | Культист пурпурной руки |
| YELLOW FANG CULTIST | Культист жёлтого клыка |

#### Корабельные термины (зоны попадания и улучшения)
| EN | RU |
|---|---|
| Hull | Корпус |
| Oars | Вёсла |
| Rigging | Такелаж |
| Steering | Руль |
| Superstructure | Надстройки |
| Ram | Таран |
| Ballista | Баллиста |
| Cannon (Medium) | Пушка (Средняя) |
| Cannon (Small) | Пушка (Малая) |
| Swivel Gun | Фальконет |
| Mortar | Мортира |
| Chain Shot (Cannon) | Книппель (пушка) |
| Grapeshot (Cannon) | Картечь (пушка) |
| Ball (Cannon) | Ядро (пушка) |
| Racing Hull | Регатный корпус |
| Luxury Cabin | Роскошная каюта |

#### Травы и зелья (из глоссария)
| EN | RU |
|---|---|
| Agurk | Агурк |
| Alfunas | Альфунас |
| Gesundheit | Гезундхайт |
| Graveroot | Могильный корень |
| Juck | Джакк |
| Mage-Leaf | Чародейский лист |
| Schlafenkraut | Шлафенкраут |
| Slowmind | Оболванщик |
| Speckled Rustwort | Крапчатый ржаволист |
| Spellwort | Чарогон |
| Spiderleaf | Паучий лист |
| Tarrabeth | Таррабет |
| Trinkwort | Трезволист |
| Valerian | Валериана |
| Vanera | Ванера |
| Vigwort | Светлолист |
| Potion of Flight | Зелье полёта |
| Ranald's Delight | «Ранальдова услада» |

#### Болезни (дополнения к основному списку)
| EN | RU |
|---|---|
| Reikworms | Рейкчервь |
| Cavity Worms | Полостные черви |
| Galloping Yellow Scumpox | Бешеная жёлтая лихорадка |
| Bleeding Eyerot | Глазная кровогниль |
| NURGLE'S ROT | Гниль Нургла |

#### Состояния и механики (дополнения)
| EN | RU |
|---|---|
| BESMIRCHED | Замаранный |
| Ammo | Боеприпасы |

---

## Сомнения в терминах

Если встречается незнакомый термин или неочевидный перевод — **спросить у пользователя**. Не искать в сторонних файлах самостоятельно.

---

## Типографика и форматирование

### Структура страниц книги
- `CaslonAntique` (7pt) — колонтитул «WARHAMMER FANTASY ROLEPLAY»
- `DwarvenAxeBB` — номер страницы
- `CaslonAntique-Bold` (19pt) — заголовок раздела [H1]
- `CaslonAntique-Bold-SC700` (12-18pt) — подзаголовок [H2]
- `ACaslonPro-Regular` (9pt) — основной текст
- `ACaslonPro-Bold` (9pt) — выделение в тексте
- `onlyskulls` — маркер списка (череп), оставлять как есть

### Правила разбивки текста
- Русский текст на ~20% длиннее английского — сокращай при необходимости, сохраняя смысл
- Колонтитулы и номера страниц НЕ переводить
- Вставные блоки (сноски, «Adventure Seeds», «GM Advice») переводить полностью

---

## Статус перевода

| Раздел | Страницы | Статус |
|---|---|---|
| Предисловие (Preface) | 3 | ✅ |
| Введение (Introduction) | 4 | ✅ |
| Ведение приключения (Running) | 4-5 | ✅ |
| Сюжет (The Story) | 6 | ✅ |
| Главы (The Chapters) | 7 | ✅ |
| Титульный разворот | 8 | ✅ |
| Покидая Богенхафен | 9 | ✅ |
| Из Богенхафена в Вайсбрюк (начало) | 10 | ✅ |
| Нападение мутантов, Лодка | 11-12 | ✅ |
| Вайсбрюк: Пурпурная Длань | 13 | ✅ |
| Вайсбрюк: дом Эльвиры | 14-15 | ✅ |
| Вайсбрюк: сарай, охотник за головами | 16-18 | ✅ |
| Из Вайсбрюка в Альтдорф | 19-20 | ✅ |
| НИП: мутанты, Ренате, Эльвира, Лиза | 21-22 | ✅ |
| НИП: речной патруль, Пурпурная Длань | 23 | ✅ |
| Красная Корона: планы, хронология | 24-26 | ✅ |
| Путь в Гриссенвальд, Сигнальная башня | 27-30 | ✅ |
| Башня: комнаты Г-З, Тайная библиотека | 31-32 | ✅ |
| Кемпербад: город, управление | 33-34 | ✅ |
| Развязка, НИП: Этелька, Тень, Айнджуллс | 35-36 | ✅ |
| НИП: Эрнст, Инженеры, Зомби, Гуль-чемпион | 37 | ✅ |
| (страница 38 — только иллюстрация) | 38 | ⬜ |
| Путь в Гриссенвальд, Жуткая находка, Гриссенвальд | 39-40 | ✅ |
| Кровная вражда, Khazid Slumbol, Аудиенция | 41-42 | ✅ |
| Друзья в нужде, Окрестные фермы, Гномы оправданы | 43 | ✅ |
| Нападения, В мёртвый час | 44 | ✅ |
| Путь к шахте, Чёрные пики | 45 | ✅ |
| Гоблины днём/ночью, таблицы | 46 | ✅ |
| Шахта: описание, обвал, НИП гоблины и волки | 47 | ✅ |
| Башня Этельки: первый этаж, комнаты 1–6 | 48 | ✅ |
| Башня: второй этаж, комнаты 7–11 | 49 | ✅ |
| Башня: комнаты 12–15, Гатбаг (стат-блок) | 50 | ✅ |
| Лаборатория, возвращение в Гриссенвальд, развязка | 51 | ✅ |
| НИП: стража, Дурак, Гурда и Хансе, жители | 52 | ✅ |
| НИП: шахтёры, Горим, Думплинг (стат-блоки) | 53 | ✅ |
| Назад в Кемпербад, Пурпурная Длань говорит | 54 | ✅ |
| Бесплодные холмы, Стир, мегалиты, мёртвая лошадь | 55 | ✅ |
| Двойной водопад, Таверна, Унтербаум | 56-57 | ✅ |
| В неизведанное, Дьявольский котёл, Голос в ночи | 58 | ✅ |
| Брунхильда, Пещера, Нападение скавенов | 59-60 | ✅ |
| Скелеты, возвращение, развязка, НИП | 61-63 | ✅ |
| Путь в Кемпербад, Пурпурная Длань, сигнальная башня | 64-67 | ✅ |
| Виттгендорф: прибытие, деревня, события дня 1–2 | 68-70 | ✅ |
| ... | 71-160 | ⬜ |

*Последнее обновление: страницы 3–37, 39–70 переведены и экспортированы в DOCX.*
