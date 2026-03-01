# 🤖 ChatBot v2.3 - OpenAI + Claude Extended Thinking

Продвинутый чат-бот с поддержкой контекста диалога, работающий через единый ProxyAPI.ru для OpenAI и Claude Extended Thinking.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-MatveiV%2FVC-black.svg)](https://github.com/MatveiV/VC)

**Ключевые возможности:**
- ✅ **История диалога** - автоматическое сохранение и загрузка между запусками
- ✅ **Два режима работы**: Thinking (Claude 4.5 Sonnet) и Normal (OpenAI)
- ✅ **Extended Thinking** - видите процесс размышления модели Claude
- ✅ **9 моделей ИИ** - выбор из OpenAI и Claude
- ✅ **Работа с файлами** - текст, изображения, код (47 форматов)
- ✅ **Vision API** - анализ изображений (gpt-4o, Claude 3.5)
- ✅ **Единый API ключ** ProxyAPI для всех сервисов
- ✅ **Обработка ошибок** - retry, таймауты, логирование
- ✅ **Конфигурация через .env** - простая настройка

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

## 🚀 Быстрый старт

### Установка

1. **Клонировать репозиторий:**
```bash
git clone https://github.com/MatveiV/VC.git
cd VC
```

2. **Создать виртуальное окружение:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Установить зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настроить .env:**
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```
Отредактируйте `.env` и добавьте ваш API ключ:
```env
PROXYAPI_KEY=your_proxyapi_key_here
```

**Получить ключ:** https://proxyapi.ru

### Проверка

```bash
# Проверка всех требований
python test_requirements.py

# Быстрый тест
python quick_test.py

# Основной чат-бот
python chat_bot.py
```

---

## 📋 Выполнение требований

### ✅ 1. История диалога
Проект автоматически сохраняет и загружает историю диалога между запусками:
```python
# Первый запуск
bot = ChatBot()
bot.chat("Привет!")
# История сохранена в chat_history.json

# Второй запуск
bot = ChatBot()
# История автоматически загружена
bot.chat("Продолжаем разговор")
```

### ✅ 2. Два режима работы

#### 2.1. Normal Mode - OpenAI Chat Completions
```python
bot = ChatBot(mode="normal")
response = bot.chat("Привет!")
print(response)  # Быстрый ответ
```

#### 2.2. Thinking Mode - Claude 4.5 Sonnet с reasoning
```python
bot = ChatBot(mode="thinking")
response = bot.chat("Объясни квантовую физику")

print(response['thinking'])   # 🧠 Процесс размышления
print(response['response'])   # 💬 Ответ
print(response['usage'])      # 📊 Статистика токенов
```

### ✅ 3. Конфигурация через .env
```env
PROXYAPI_KEY=your_api_key_here
```

### ✅ 4. Обработка ошибок и таймаутов
```python
bot = ChatBot(
    timeout=60,        # Таймаут запросов
    max_retries=3      # Повторные попытки
)
```

### ✅ 5. Понятные логи запуска
```
2026-03-01 22:37:29 - INFO - Инициализация ChatBot через ProxyAPI.ru
2026-03-01 22:37:29 - INFO - ✓ API ключ загружен из конфигурации
2026-03-01 22:37:30 - INFO - ✓ OpenAI клиент инициализирован
2026-03-01 22:37:30 - INFO - ✓ Режим работы: thinking
2026-03-01 22:37:30 - INFO - ✓ Claude модель: claude-sonnet-4-20250514
```

---

## 💻 Использование

### Основной чат-бот

```bash
python chat_bot.py
```

Выберите режим работы:
- **1** - Thinking Mode (Claude Extended Thinking) [По умолчанию]
- **2** - Normal Mode (OpenAI)

Команды в чате:
- `выход` - завершить
- `сброс` - очистить историю
- `режим` - сменить режим

### В коде

```python
from chat_bot import ChatBot

# Thinking Mode (Claude)
bot = ChatBot(mode="thinking")
response = bot.chat("Решите уравнение: 2x + 5 = 15")

print(response['thinking'])   # Процесс размышления
print(response['response'])   # Ответ: x = 5

# Normal Mode (OpenAI)
bot = ChatBot(mode="normal", model="gpt-4o")
response = bot.chat("Привет!")
print(response)

# Работа с файлами
response = bot.chat("Объясни этот код", file_path="script.py")

# Анализ изображения (для моделей с vision)
bot.set_model("gpt-4o")
response = bot.chat("Что на картинке?", file_path="photo.jpg")
```

---

## 🎯 Доступные модели

### OpenAI Models
| Модель | Возможности | Контекст |
|--------|-------------|----------|
| **gpt-4o** | 🖼️ Vision | 128K |
| **gpt-4-turbo** | 🖼️ Vision | 128K |
| **gpt-4** | - | 8K |
| **gpt-3.5-turbo** | - | 16K |

### Claude Models
| Модель | Возможности | Контекст |
|--------|-------------|----------|
| **claude-sonnet-4-20250514** | 💭 Thinking | 200K |
| **claude-3-5-sonnet-20241022** | 🖼️ Vision | 200K |
| **claude-3-opus-20240229** | 🖼️ Vision | 200K |
| **claude-3-sonnet-20240229** | 🖼️ Vision | 200K |
| **claude-3-haiku-20240307** | - | 200K |

**Легенда:**
- 💭 - Extended Thinking (процесс размышления)
- 🖼️ - Vision (анализ изображений)

```bash
# Список всех моделей
python models_config.py
```

---

## 📁 Поддерживаемые форматы файлов

### Текстовые (34 формата)
```
.py .js .ts .jsx .tsx .java .cpp .c .h .go .rs .rb .php .sh .bat .sql
.json .xml .yaml .yml .toml .ini .csv .html .css .scss .sass
.txt .md .r .m .swift .kt .hpp
```

### Изображения (6 форматов)
```
.jpg .jpeg .png .gif .bmp .webp
```

```bash
# Список всех форматов
python file_handler.py
```

---

## 🧪 Тестирование

```bash
# Проверка всех требований
python test_requirements.py

# Тест моделей и файлов
python test_models_and_files.py

# Тест сохранения истории
python test_persistence.py

# Интерактивная демонстрация
python demo_models_and_files.py
```

---

## 📚 Документация

- [DEPLOYMENT_REPORT.md](DEPLOYMENT_REPORT.md) - 📋 Отчет о выполнении требований
- [CHANGELOG.md](CHANGELOG.md) - 📝 История изменений
- [V2.3_FEATURES_REPORT.md](V2.3_FEATURES_REPORT.md) - 📊 Отчет о версии 2.3
- [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md) - 🧠 Интеграция Claude
- [API_REFERENCE.md](API_REFERENCE.md) - 📖 Справочник API
- [ARCHITECTURE.md](ARCHITECTURE.md) - 🏗️ Архитектура системы

[Полный индекс документации](DOCUMENTATION_INDEX.md)

---

## 🏗️ Структура проекта

```
VC/
├── chat_bot.py              # Главный класс ChatBot
├── testagent.py             # Claude Extended Thinking API
├── models_config.py         # Конфигурация 9 моделей
├── file_handler.py          # Работа с файлами
├── test_requirements.py     # Проверка требований ✅
├── test_*.py                # Тесты
├── demo_*.py                # Демонстрации
├── requirements.txt         # Зависимости
├── .env.example             # Шаблон конфигурации
└── docs/                    # Документация (15 файлов)
```

---

## 🔧 Технологии

- **Python 3.8+**
- **OpenAI API** через ProxyAPI.ru
- **Anthropic Claude API** через ProxyAPI.ru
- **python-dotenv** для конфигурации
- **logging** для логирования

---

## 📊 Статистика

- **9 моделей ИИ** (4 OpenAI + 5 Claude)
- **47 форматов файлов** (34 текст + 6 изображения + 7 документы)
- **15 документов** с полным описанием
- **11 тестов** для проверки функциональности
- **2 режима работы** (Normal + Thinking)

---

## 🤝 Вклад

Проект разработан на уровне senior developer с полной документацией и тестированием.

---

## 📄 Лицензия

MIT License

---

## 🔗 Ссылки

- **GitHub:** https://github.com/MatveiV/VC
- **ProxyAPI:** https://proxyapi.ru
- **OpenAI:** https://openai.com
- **Anthropic:** https://anthropic.com

---

## ✅ Проверка требований

Все требования выполнены и протестированы:

```bash
python test_requirements.py
```

**Результат:**
```
✅ ВСЕ ТРЕБОВАНИЯ ВЫПОЛНЕНЫ!

📋 ИТОГИ:
  ✓ История диалога сохраняется и загружается
  ✓ Два режима: Normal (OpenAI) и Thinking (Claude 4.5 Sonnet)
  ✓ Конфигурация через .env файл
  ✓ Обработка ошибок и таймаутов
  ✓ Понятные логи запуска

🚀 ПРОЕКТ ГОТОВ К ИСПОЛЬЗОВАНИЮ!
```

---

**Версия:** 2.3  
**Дата:** 2026-03-01  
**Автор:** Senior Developer
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
