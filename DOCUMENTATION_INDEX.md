# 📚 Индекс документации

## 🚀 Начало работы

### Для новичков
1. [README.md](README.md) - Главная страница проекта
2. [QUICKSTART.md](QUICKSTART.md) - Быстрый старт с OpenAI (3 шага)
3. [QUICKSTART_CLAUDE.md](QUICKSTART_CLAUDE.md) - Быстрый старт с Claude (5 минут)

### Для разработчиков
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура системы
2. [API_REFERENCE.md](API_REFERENCE.md) - Справочник по API
3. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Структура проекта

## 🧠 Claude Extended Thinking

### Основное
- [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md) - Полное руководство по интеграции
- [EXAMPLES_CLAUDE.md](EXAMPLES_CLAUDE.md) - 10 примеров использования

### Дополнительно
- `testagent.py` - Исходный код модуля
- `test_claude_integration.py` - Тесты интеграции

## 📖 Справочная информация

### Возможности
- [FEATURES.md](FEATURES.md) - Подробное описание всех возможностей
- [SUMMARY.md](SUMMARY.md) - Итоговый обзор проекта

### История
- [CHANGELOG.md](CHANGELOG.md) - История изменений
- [FILES.md](FILES.md) - Список всех файлов

## 🎯 По задачам

### Хочу быстро начать
→ [QUICKSTART_CLAUDE.md](QUICKSTART_CLAUDE.md)

### Хочу понять как работает
→ [ARCHITECTURE.md](ARCHITECTURE.md)

### Хочу примеры кода
→ [EXAMPLES_CLAUDE.md](EXAMPLES_CLAUDE.md)

### Хочу справочник по функциям
→ [API_REFERENCE.md](API_REFERENCE.md)

### Хочу узнать что нового
→ [CHANGELOG.md](CHANGELOG.md)

### Хочу понять структуру
→ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 📂 Структура документации

```
docs/
├── README.md                    # Главная страница
├── QUICKSTART.md                # Быстрый старт (OpenAI)
├── QUICKSTART_CLAUDE.md         # Быстрый старт (Claude)
│
├── CLAUDE_INTEGRATION.md        # Руководство по Claude
├── EXAMPLES_CLAUDE.md           # Примеры Claude
├── API_REFERENCE.md             # Справочник API
├── ARCHITECTURE.md              # Архитектура
│
├── FEATURES.md                  # Возможности
├── PROJECT_STRUCTURE.md         # Структура проекта
├── FILES.md                     # Список файлов
│
├── CHANGELOG.md                 # История изменений
├── SUMMARY.md                   # Итоговый обзор
└── DOCUMENTATION_INDEX.md       # Этот файл
```

## 🔍 Поиск по темам

### API Keys
- [QUICKSTART.md](QUICKSTART.md#установка) - Настройка ключей
- [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md#конфигурация) - Ключи Claude

### Режимы работы
- [README.md](README.md#режимы-работы) - Обзор режимов
- [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md#что-такое-extended-thinking) - Thinking Mode
- [ARCHITECTURE.md](ARCHITECTURE.md#mode-selection--routing) - Логика выбора

### Примеры использования
- [EXAMPLES_CLAUDE.md](EXAMPLES_CLAUDE.md) - 10 примеров
- [QUICKSTART_CLAUDE.md](QUICKSTART_CLAUDE.md#использование-в-коде) - Быстрые примеры
- [API_REFERENCE.md](API_REFERENCE.md) - Примеры в справочнике

### Сохранение контекста
- [FEATURES.md](FEATURES.md#сохранение-контекста-диалога) - Описание
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#сохранение-контекста) - Примеры

### Troubleshooting
- [QUICKSTART_CLAUDE.md](QUICKSTART_CLAUDE.md#troubleshooting) - Решение проблем
- [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md#troubleshooting) - Подробное руководство

### Тестирование
- [FILES.md](FILES.md#тестовые-файлы) - Список тестов
- `test_claude_integration.py` - Тест интеграции
- `test_persistence.py` - Тест сохранения

## 📊 Документация по уровням

### Уровень 1: Начинающий
```
README.md
    ↓
QUICKSTART_CLAUDE.md
    ↓
EXAMPLES_CLAUDE.md (примеры 1-3)
```

### Уровень 2: Продвинутый
```
CLAUDE_INTEGRATION.md
    ↓
API_REFERENCE.md
    ↓
EXAMPLES_CLAUDE.md (примеры 4-7)
```

### Уровень 3: Эксперт
```
ARCHITECTURE.md
    ↓
PROJECT_STRUCTURE.md
    ↓
EXAMPLES_CLAUDE.md (примеры 8-10)
    ↓
Исходный код
```

## 🎓 Учебные треки

### Трек 1: Быстрый старт (30 минут)
1. README.md (5 мин)
2. QUICKSTART_CLAUDE.md (10 мин)
3. Запуск `test_claude_integration.py` (5 мин)
4. Запуск `testagent.py` (5 мин)
5. Интерактивный режим `test_chat.py` (5 мин)

### Трек 2: Глубокое погружение (2 часа)
1. CLAUDE_INTEGRATION.md (30 мин)
2. EXAMPLES_CLAUDE.md (30 мин)
3. API_REFERENCE.md (30 мин)
4. Практика с примерами (30 мин)

### Трек 3: Мастер-класс (4 часа)
1. ARCHITECTURE.md (60 мин)
2. Изучение исходного кода (90 мин)
3. Создание своих примеров (60 мин)
4. Интеграция в проект (30 мин)

## 🔗 Внешние ресурсы

### Anthropic
- [Документация Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Anthropic Console](https://console.anthropic.com/)
- [API Reference](https://docs.anthropic.com/en/api)

### OpenAI
- [OpenAI API Docs](https://platform.openai.com/docs)
- [ProxyAPI.ru](https://proxyapi.ru)
- [ProxyAPI Docs](https://proxyapi.ru/docs)

### Python
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [anthropic SDK](https://pypi.org/project/anthropic/)
- [openai SDK](https://pypi.org/project/openai/)

## 📝 Как читать документацию

### Формат документов

**Markdown файлы:**
- `#` - Главный заголовок
- `##` - Раздел
- `###` - Подраздел
- `` `code` `` - Код в тексте
- ` ```python ` - Блок кода

**Эмодзи:**
- 🚀 - Начало работы
- 🧠 - Claude / Thinking
- ⚡ - OpenAI / Normal
- ✅ - Успех / Готово
- ⚠️ - Внимание / Предупреждение
- 📚 - Документация
- 🔧 - Конфигурация
- 🎯 - Примеры / Практика

### Навигация

**Внутренние ссылки:**
```markdown
[Текст ссылки](FILE.md#раздел)
```

**Внешние ссылки:**
```markdown
[Текст ссылки](https://example.com)
```

## 🆘 Получение помощи

### Порядок действий

1. **Проверьте FAQ** в соответствующем документе
2. **Запустите тесты** для диагностики
3. **Изучите примеры** похожих задач
4. **Проверьте конфигурацию** (API ключи, .env)

### Где искать ответы

| Вопрос | Документ |
|--------|----------|
| Как установить? | QUICKSTART_CLAUDE.md |
| Как использовать? | EXAMPLES_CLAUDE.md |
| Что это за функция? | API_REFERENCE.md |
| Почему не работает? | QUICKSTART_CLAUDE.md#troubleshooting |
| Как это устроено? | ARCHITECTURE.md |
| Что нового? | CHANGELOG.md |

## 📈 Обновления документации

### Версия 2.1 (текущая)
- ✅ Добавлена документация по Claude
- ✅ Создан индекс документации
- ✅ Добавлены примеры использования
- ✅ Описана архитектура

### Планы
- [ ] Видео-туториалы
- [ ] Интерактивные примеры
- [ ] Перевод на английский
- [ ] API документация в Swagger

## 🎯 Следующие шаги

После изучения документации:

1. **Попробуйте примеры** из EXAMPLES_CLAUDE.md
2. **Интегрируйте в свой проект** используя API_REFERENCE.md
3. **Изучите архитектуру** для глубокого понимания
4. **Экспериментируйте** с разными режимами и настройками

---

**Документация обновлена:** 2026-03-01  
**Версия проекта:** 2.1  
**Всего документов:** 13
