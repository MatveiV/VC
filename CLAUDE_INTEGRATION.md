# 🧠 Интеграция Claude Extended Thinking API

## Обзор

Проект теперь поддерживает два режима работы:

1. **Thinking Mode** (по умолчанию) - использует Claude Extended Thinking API от Anthropic
2. **Normal Mode** - использует OpenAI API через ProxyAPI.ru

## Что такое Extended Thinking?

Extended Thinking - это новая возможность от Anthropic, которая позволяет модели Claude "думать" перед ответом. Модель показывает свой процесс размышления, что делает ответы более обоснованными и точными.

### Преимущества думающей модели:

- 🧠 **Прозрачность мышления** - видите процесс рассуждения модели
- 🎯 **Более точные ответы** - модель анализирует задачу перед ответом
- 📊 **Контроль бюджета** - можно ограничить токены для размышлений
- 🔍 **Лучше для сложных задач** - математика, логика, анализ

## Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                      test_chat.py                           │
│                    (Основной файл)                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Выбор режима при запуске                            │  │
│  │  • Thinking Mode (Claude) - по умолчанию             │  │
│  │  • Normal Mode (OpenAI)                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│         ┌────────────────┴────────────────┐                │
│         │                                  │                │
│         ▼                                  ▼                │
│  ┌─────────────┐                   ┌─────────────┐         │
│  │  testagent  │                   │   OpenAI    │         │
│  │   (Claude)  │                   │  (ProxyAPI) │         │
│  └─────────────┘                   └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Конфигурация

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

Новые зависимости:
- `anthropic>=0.40.0` - SDK для работы с Claude API

### 2. Настройка API ключей

Создайте файл `.env`:

```env
# OpenAI через ProxyAPI
PROXYAPI_KEY=your_proxyapi_key_here

# Claude от Anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
```

Получить ключи:
- ProxyAPI: https://proxyapi.ru
- Anthropic: https://console.anthropic.com/

### 3. Параметры конфигурации

В `test_chat.py`:

```python
# Модель Claude (думающая версия)
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Бюджет токенов для размышлений (default=1500)
THINKING_BUDGET = 1500

# Режим по умолчанию
CURRENT_MODE = "thinking"  # или "normal"
```

## Использование

### Интерактивный режим

```bash
python test_chat.py
```

При запуске выберите режим:
```
🤖 ВЫБОР РЕЖИМА РАБОТЫ:
1. Thinking Mode (Claude Extended Thinking) - думающая модель [По умолчанию]
2. Normal Mode (OpenAI через ProxyAPI) - обычная модель

Выберите режим (1/2, Enter=1):
```

### Команды в чате

- `выход` / `exit` / `quit` - завершить работу
- `сброс` / `reset` - очистить историю диалога
- `режим` / `mode` - переключить режим работы

### Программное использование

#### Вариант 1: Через test_chat.py

```python
from test_chat import generate_response, CURRENT_MODE

# Thinking Mode (Claude)
CURRENT_MODE = "thinking"
result = generate_response("Объясни квантовую запутанность")

# Результат содержит:
print(result['thinking'])   # Процесс размышления
print(result['response'])   # Финальный ответ
print(result['usage'])      # Статистика токенов

# Normal Mode (OpenAI)
CURRENT_MODE = "normal"
response = generate_response("Привет!")
print(response)  # Просто строка
```

#### Вариант 2: Через testagent.py напрямую

```python
from testagent import chat_with_thinking_model, format_thinking_response

# Простой запрос
result = chat_with_thinking_model(
    user_message="Решите уравнение: 2x + 5 = 15",
    thinking_budget=2000
)

# Красивый вывод
print(format_thinking_response(result))
```

#### Вариант 3: Через ChatBot класс

```python
from chat_bot import ChatBot

# Создание бота в режиме thinking
bot = ChatBot(
    mode="thinking",
    claude_model="claude-sonnet-4-20250514",
    thinking_budget=1500
)

# Отправка сообщения
result = bot.chat("Объясни теорему Пифагора")

# Результат - dict с полной информацией
print(result['thinking'])   # Процесс размышления
print(result['response'])   # Ответ
```

## Формат ответа

### Thinking Mode (Claude)

```python
{
    'response': 'Финальный ответ модели',
    'thinking': 'Процесс размышления модели (может быть None)',
    'usage': {
        'input_tokens': 39,
        'output_tokens': 65,
        'total_tokens': 104
    },
    'full_message': <объект Message от Anthropic>,
    'model': 'claude-sonnet-4-20250514',
    'stop_reason': 'end_turn'
}
```

### Normal Mode (OpenAI)

```python
"Просто текстовый ответ"
```

## Примеры вывода

### Пример 1: Простой вопрос

**Вход:**
```
Вы: Привет! Как дела?
```

**Выход (Thinking Mode):**
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

### Пример 2: Сложная задача

**Вход:**
```
Вы: Объясни разницу между async/await и threading в Python
```

**Выход (Thinking Mode):**
```
======================================================================
🧠 ПРОЦЕСС РАЗМЫШЛЕНИЯ:
----------------------------------------------------------------------
The user is asking about the difference between async/await and 
threading in Python. This is a technical question about concurrency 
models.

Key points to cover:
1. Threading uses OS threads (preemptive multitasking)
2. Async/await uses cooperative multitasking (event loop)
3. Threading is better for CPU-bound tasks
4. Async/await is better for I/O-bound tasks
5. GIL limitations in Python
----------------------------------------------------------------------

💬 ОТВЕТ:
----------------------------------------------------------------------
[Подробный ответ с объяснением различий...]
----------------------------------------------------------------------
```

## Настройка бюджета токенов

Бюджет токенов контролирует, сколько модель может "думать":

```python
# Минимальный бюджет (быстрые ответы)
thinking_budget=500

# Стандартный бюджет (по умолчанию)
thinking_budget=1500

# Большой бюджет (сложные задачи)
thinking_budget=3000

# Максимальный бюджет
thinking_budget=5000
```

### Рекомендации:

- **500-1000** - простые вопросы, приветствия
- **1500-2000** - стандартные задачи, объяснения
- **2500-3500** - сложные задачи, анализ, математика
- **4000-5000** - очень сложные задачи, требующие глубокого анализа

## Доступные модели Claude

### Думающие модели (Extended Thinking):

- `claude-sonnet-4-20250514` - рекомендуется (по умолчанию)
- `claude-sonnet-4-5-20250929` - альтернативная версия

### Обычные модели:

- `claude-3-5-sonnet-20241022` - быстрая модель без thinking
- `claude-3-opus-20240229` - мощная модель

## Сравнение режимов

| Характеристика | Thinking Mode (Claude) | Normal Mode (OpenAI) |
|----------------|------------------------|----------------------|
| Прозрачность | ✅ Показывает процесс мышления | ❌ Только ответ |
| Скорость | 🐢 Медленнее (думает) | 🚀 Быстрее |
| Точность | 🎯 Выше для сложных задач | ⚡ Хорошо для простых |
| Стоимость | 💰 Дороже (больше токенов) | 💵 Дешевле |
| Контекст | 📚 До 200K токенов | 📖 До 128K токенов |
| Языки | 🌍 Отлично для всех | 🌍 Отлично для всех |

## Обработка ошибок

Система автоматически переключается на Normal Mode при ошибках:

```python
try:
    # Попытка использовать Claude
    result = generate_response("Привет", mode="thinking")
except Exception as e:
    print(f"⚠️  Ошибка в режиме thinking: {e}")
    print("Переключаюсь на обычный режим...")
    # Автоматически использует OpenAI
```

## Тестирование

### Тест testagent.py

```bash
python testagent.py
```

Запускает два теста:
1. Простой вопрос
2. Сложная задача требующая размышления

### Тест интеграции

```bash
python test_chat.py
```

Выберите режим "1" (Thinking Mode) и попробуйте:
- Простые вопросы
- Сложные задачи
- Переключение режимов командой `режим`

## Лучшие практики

### 1. Выбор режима

**Используйте Thinking Mode для:**
- Математических задач
- Логических головоломок
- Анализа кода
- Сложных объяснений
- Принятия решений

**Используйте Normal Mode для:**
- Простых вопросов
- Приветствий
- Быстрых ответов
- Генерации текста

### 2. Оптимизация бюджета

```python
# Адаптивный бюджет в зависимости от задачи
if "математика" in user_message or "решите" in user_message:
    thinking_budget = 3000
elif "объясни" in user_message:
    thinking_budget = 2000
else:
    thinking_budget = 1500
```

### 3. Сохранение истории

История сохраняется автоматически для обоих режимов:

```python
# История совместима между режимами
bot = ChatBot(mode="thinking")
bot.chat("Привет")

# Переключаем режим
bot.set_mode("normal")
bot.chat("Продолжаем")  # История сохранена
```

## Troubleshooting

### Проблема: Claude недоступен

```
⚠️  testagent.py не найден. Думающая модель Claude недоступна.
```

**Решение:**
1. Убедитесь что файл `testagent.py` существует
2. Проверьте что `anthropic` установлен: `pip install anthropic`

### Проблема: Ошибка API ключа

```
⚠️  ВНИМАНИЕ: Установите ANTHROPIC_API_KEY в .env файле
```

**Решение:**
1. Создайте файл `.env`
2. Добавьте `ANTHROPIC_API_KEY=your_key_here`
3. Получите ключ на https://console.anthropic.com/

### Проблема: Автоматическое переключение на Normal Mode

```
⚠️  Ошибка в режиме thinking: ...
Переключаюсь на обычный режим...
```

**Причины:**
- Неверный API ключ
- Превышен лимит запросов
- Проблемы с сетью

**Решение:**
- Проверьте API ключ
- Проверьте баланс аккаунта Anthropic
- Проверьте интернет соединение

## Стоимость

### Claude Extended Thinking

Стоимость зависит от модели и количества токенов:

- **Input tokens**: ~$3 за 1M токенов
- **Output tokens**: ~$15 за 1M токенов
- **Thinking tokens**: считаются как output

Пример расчета:
```
Запрос: 100 input + 50 thinking + 100 output = 250 токенов
Стоимость: (100 * $3 + 150 * $15) / 1,000,000 = $0.00255
```

### OpenAI через ProxyAPI

Стоимость зависит от тарифов ProxyAPI.ru

## Дополнительные ресурсы

- [Документация Anthropic Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Anthropic Console](https://console.anthropic.com/)
- [ProxyAPI.ru](https://proxyapi.ru)
- [Примеры использования](EXAMPLES_CLAUDE.md)

## Changelog

### v2.1.0 - Интеграция Claude Extended Thinking
- ✅ Добавлена поддержка Claude Extended Thinking API
- ✅ Режим переключения между thinking и normal
- ✅ Настройка бюджета токенов для размышлений
- ✅ Красивое форматирование вывода с процессом мышления
- ✅ Автоматический fallback на OpenAI при ошибках
- ✅ Полная документация и примеры
