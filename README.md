# OpenAI Chat Bot через ProxyAPI.ru + Claude Extended Thinking

Продвинутый чат-бот с поддержкой контекста диалога, работающий через единый ProxyAPI.ru для OpenAI и Claude Extended Thinking.

**Ключевые возможности:**
- ✅ Выбор из 9 моделей ИИ (OpenAI + Claude)
- ✅ Работа с файлами (текст, изображения, код)
- ✅ Два режима работы: Thinking (Claude) и Normal (OpenAI)
- ✅ Единый API ключ ProxyAPI для всех сервисов
- ✅ Extended Thinking - видите процесс размышления модели
- ✅ Vision API - анализ изображений (gpt-4o, Claude 3.5)
- ✅ Автоматическое сохранение и загрузка истории диалога
- ✅ Бот помнит предыдущие разговоры между запусками
- ✅ Настройка бюджета токенов для размышлений
- ✅ Поддержка системных промптов
- ✅ Интерактивный и программный режимы

📚 **Документация:**
- [PROXYAPI_MIGRATION.md](PROXYAPI_MIGRATION.md) - 🔄 Миграция на единый ProxyAPI (v2.2)
- [SENIOR_DEVELOPER_REPORT.md](SENIOR_DEVELOPER_REPORT.md) - 📋 Отчет о выполненной работе
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - 📚 Индекс всей документации
- [QUICKSTART.md](QUICKSTART.md) - Быстрый старт за 3 шага (OpenAI)
- [QUICKSTART_CLAUDE.md](QUICKSTART_CLAUDE.md) - Быстрый старт с Claude Extended Thinking
- [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md) - Полное руководство по Claude Extended Thinking
- [EXAMPLES_CLAUDE.md](EXAMPLES_CLAUDE.md) - Примеры использования думающей модели
- [API_REFERENCE.md](API_REFERENCE.md) - Справочник по API
- [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура системы
- [FEATURES.md](FEATURES.md) - Подробное описание возможностей
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Структура проекта
- [FILES.md](FILES.md) - Список всех файлов проекта
- [CHANGELOG.md](CHANGELOG.md) - История изменений
- [SUMMARY.md](SUMMARY.md) - Итоговый обзор

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` (скопируйте из `.env.example`) и добавьте ваш API ключ от ProxyAPI:
```
PROXYAPI_KEY=your_proxyapi_key_here
```

**Важно:** Используется единый ключ ProxyAPI для доступа к OpenAI и Claude!

Получить ключ: https://proxyapi.ru

Получить API ключ можно на https://proxyapi.ru

## Использование

### Режимы работы

Проект поддерживает два режима:

1. **Thinking Mode** (по умолчанию) - Claude Extended Thinking
   - Показывает процесс размышления модели
   - Лучше для сложных задач
   - Настраиваемый бюджет токенов

2. **Normal Mode** - OpenAI через ProxyAPI
   - Быстрые ответы
   - Хорошо для простых задач
   - Дешевле

### Быстрый старт

Быстрый тест работоспособности:
```bash
python quick_test.py
```

Тест выбора моделей и работы с файлами:
```bash
python test_models_and_files.py
```

Интерактивная демонстрация:
```bash
python demo_models_and_files.py
```

Список всех моделей:
```bash
python models_config.py
```

Список поддерживаемых форматов файлов:
```bash
python file_handler.py
```

Тест сохранения контекста между запусками:
```bash
python test_persistence.py
# или более простой тест
python test_save_load.py
```

Запустите основной чат-бот:
```bash
python chat_bot.py
```

Или запустите тестовый файл с выбором режима:
```bash
python test_chat.py
```

## Сохранение контекста

Все приложения автоматически сохраняют историю диалога в JSON файлы:
- `chat_bot.py` → `chat_history.json`
- `test_chat.py` → `test_chat_history.json`
- `demo_persistence.py` → `demo_history.json`

При следующем запуске история автоматически загружается, и бот помнит предыдущий разговор.

Для очистки истории используйте команду `сброс` в интерактивном режиме.

## Демонстрация

Запустите `demo_persistence.py` несколько раз подряд:
```bash
python demo_persistence.py
```

Вы увидите, как бот помнит предыдущие разговоры между запусками программы!

## Пример вывода Claude Extended Thinking

```
======================================================================
Модель: claude-sonnet-4-20250514
======================================================================

🧠 ПРОЦЕСС РАЗМЫШЛЕНИЯ:
----------------------------------------------------------------------
The user has greeted me in Russian, saying "Привет!" which means 
"Hello!" or "Hi!"

I should respond in a friendly way in Russian.
----------------------------------------------------------------------

💬 ОТВЕТ:
----------------------------------------------------------------------
Привет! Как дела? Чем могу помочь?
----------------------------------------------------------------------

📊 СТАТИСТИКА:
  • Входные токены: 39
  • Выходные токены: 65
  • Всего токенов: 104
  • Причина остановки: end_turn
======================================================================
```

Используйте в своем коде:

#### Вариант 1: ChatBot класс (рекомендуется)

```python
from chat_bot import ChatBot

# Создание бота с выбором модели
bot = ChatBot(model="gpt-4o")  # Модель с vision

# Обычный диалог
response = bot.chat("Привет!")
print(response)

# Анализ текстового файла
response = bot.chat("Объясни этот код", file_path="script.py")
print(response)

# Анализ изображения (для моделей с vision)
response = bot.chat("Что на картинке?", file_path="photo.jpg")
print(response)

# Смена модели
bot.set_model("claude-3-5-sonnet-20241022")
response = bot.chat("Продолжаем разговор")

# Список доступных моделей
bot.list_available_models()
```

#### Вариант 2: Функции из test_chat.py

```python
from test_chat import generate_response

# Thinking Mode
result = generate_response("Решите уравнение: 2x + 5 = 15", mode="thinking")
print(result['thinking'])
print(result['response'])

# Normal Mode
response = generate_response("Привет!", mode="normal")
print(response)
```

#### Вариант 3: Прямое использование testagent.py

```python
from testagent import chat_with_thinking_model, format_thinking_response

result = chat_with_thinking_model(
    "Объясни теорию относительности",
    thinking_budget=2500
)

# Красивый вывод
print(format_thinking_response(result))
```
