# 📖 API Reference

## testagent.py

### chat_with_thinking_model()

Основная функция для взаимодействия с Claude Extended Thinking API.

```python
def chat_with_thinking_model(
    user_message: str,
    conversation_history: list = None,
    model: str = "claude-sonnet-4-20250514",
    thinking_budget: int = 1500,
    system_prompt: str = None
) -> dict
```

**Параметры:**

- `user_message` (str, обязательный): Сообщение пользователя
- `conversation_history` (list, опционально): История диалога в формате `[{"role": "user", "content": "..."}, ...]`
- `model` (str, опционально): Модель Claude для использования (default: "claude-sonnet-4-20250514")
- `thinking_budget` (int, опционально): Бюджет токенов для размышлений (default: 1500)
- `system_prompt` (str, опционально): Системный промпт для настройки поведения

**Возвращает:**

```python
{
    'response': str,           # Текст ответа
    'thinking': str | None,    # Процесс размышления (может быть None)
    'usage': {
        'input_tokens': int,
        'output_tokens': int,
        'total_tokens': int
    },
    'full_message': Message,   # Полный объект ответа от Anthropic
    'model': str,              # Использованная модель
    'stop_reason': str         # Причина остановки генерации
}
```

**Пример:**

```python
result = chat_with_thinking_model(
    user_message="Объясни квантовую физику",
    thinking_budget=2000,
    system_prompt="Ты учитель физики"
)
```

---

### format_thinking_response()

Форматирует ответ от думающей модели в красивый текст.

```python
def format_thinking_response(result: dict) -> str
```

**Параметры:**

- `result` (dict): Результат от `chat_with_thinking_model()`

**Возвращает:**

- `str`: Отформатированный текст с разделами для размышления, ответа и статистики

**Пример:**

```python
result = chat_with_thinking_model("Привет!")
formatted = format_thinking_response(result)
print(formatted)
```

---

## test_chat.py

### generate_response()

Универсальная функция генерации ответа с поддержкой двух режимов.

```python
def generate_response(
    user_message: str,
    system_prompt: str = None,
    auto_save: bool = True,
    mode: str = None
) -> str | dict
```

**Параметры:**

- `user_message` (str, обязательный): Сообщение пользователя
- `system_prompt` (str, опционально): Системный промпт (только для первого сообщения)
- `auto_save` (bool, опционально): Автоматически сохранять историю (default: True)
- `mode` (str, опционально): Режим работы ("thinking" или "normal", если None - использует CURRENT_MODE)

**Возвращает:**

- `dict` - для thinking mode (с полной информацией)
- `str` - для normal mode (только текст ответа)

**Пример:**

```python
# Thinking mode
result = generate_response("Объясни рекурсию", mode="thinking")
print(result['thinking'])
print(result['response'])

# Normal mode
response = generate_response("Привет", mode="normal")
print(response)
```

---

### chat_loop()

Запускает интерактивный диалог с выбором режима.

```python
def chat_loop() -> None
```

**Параметры:** Нет

**Возвращает:** None

**Особенности:**

- Выбор режима при запуске
- Команды: `выход`, `сброс`, `режим`
- Автоматическое сохранение истории
- Красивое форматирование вывода

**Пример:**

```python
from test_chat import chat_loop

chat_loop()
```

---

### Вспомогательные функции

#### add_message()

```python
def add_message(role: str, content: str) -> None
```

Добавляет сообщение в глобальную историю диалога.

#### save_history()

```python
def save_history() -> None
```

Сохраняет историю диалога в JSON файл.

#### load_history()

```python
def load_history() -> None
```

Загружает историю диалога из JSON файла.

#### reset_conversation()

```python
def reset_conversation() -> None
```

Очищает историю диалога и удаляет файл истории.

---

## chat_bot.py

### ChatBot

Класс для работы с чат-ботом с поддержкой двух режимов.

```python
class ChatBot:
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-3.5-turbo",
        history_file: str = "chat_history.json",
        mode: str = "thinking",
        claude_model: str = "claude-sonnet-4-20250514",
        thinking_budget: int = 1500,
        anthropic_key: str = None
    )
```

**Параметры:**

- `api_key` (str, опционально): API ключ ProxyAPI (из env если None)
- `model` (str, опционально): Модель OpenAI (default: "gpt-3.5-turbo")
- `history_file` (str, опционально): Файл для истории (default: "chat_history.json")
- `mode` (str, опционально): Режим работы (default: "thinking")
- `claude_model` (str, опционально): Модель Claude (default: "claude-sonnet-4-20250514")
- `thinking_budget` (int, опционально): Бюджет токенов (default: 1500)
- `anthropic_key` (str, опционально): API ключ Anthropic (из env если None)

**Методы:**

#### chat()

```python
def chat(self, user_message: str, auto_save: bool = True) -> str | dict
```

Отправляет сообщение и получает ответ.

**Возвращает:**
- `dict` для thinking mode
- `str` для normal mode

#### set_system_prompt()

```python
def set_system_prompt(self, system_message: str) -> None
```

Устанавливает системный промпт.

#### set_mode()

```python
def set_mode(self, mode: str) -> None
```

Переключает режим работы ("thinking" или "normal").

#### get_mode()

```python
def get_mode(self) -> str
```

Возвращает текущий режим работы.

#### reset_conversation()

```python
def reset_conversation(self) -> None
```

Очищает историю диалога.

#### save_history()

```python
def save_history(self) -> None
```

Сохраняет историю в файл.

#### load_history()

```python
def load_history(self) -> None
```

Загружает историю из файла.

**Пример использования:**

```python
from chat_bot import ChatBot

# Создание бота
bot = ChatBot(
    mode="thinking",
    thinking_budget=2000
)

# Настройка
bot.set_system_prompt("Ты помощник программиста")

# Диалог
result = bot.chat("Объясни декораторы в Python")
print(result['response'])

# Переключение режима
bot.set_mode("normal")
response = bot.chat("Спасибо")
print(response)

# Очистка истории
bot.reset_conversation()
```

---

## Глобальные переменные

### test_chat.py

```python
API_KEY: str                    # Ключ ProxyAPI
BASE_URL: str                   # URL ProxyAPI
MODEL: str                      # Модель OpenAI
HISTORY_FILE: str               # Файл истории
ANTHROPIC_API_KEY: str          # Ключ Anthropic
CLAUDE_MODEL: str               # Модель Claude
THINKING_BUDGET: int            # Бюджет токенов
CURRENT_MODE: str               # Текущий режим
CLAUDE_AVAILABLE: bool          # Доступность Claude
conversation_history: list      # История диалога
```

### testagent.py

```python
ANTHROPIC_API_KEY: str          # Ключ Anthropic
DEFAULT_MODEL: str              # Модель по умолчанию
DEFAULT_THINKING_BUDGET: int    # Бюджет по умолчанию
```

---

## Типы данных

### Message (от Anthropic)

```python
Message(
    id: str,
    content: List[ContentBlock],
    model: str,
    role: str,
    stop_reason: str,
    stop_sequence: Optional[str],
    type: str,
    usage: Usage
)
```

### ContentBlock

```python
# ThinkingBlock
ThinkingBlock(
    type: "thinking",
    thinking: str,
    signature: str
)

# TextBlock
TextBlock(
    type: "text",
    text: str
)
```

### Usage

```python
Usage(
    input_tokens: int,
    output_tokens: int,
    cache_creation_input_tokens: int,
    cache_read_input_tokens: int
)
```

---

## Константы

### Модели Claude

```python
THINKING_MODELS = [
    "claude-sonnet-4-20250514",      # Рекомендуется
    "claude-sonnet-4-5-20250929"     # Альтернатива
]

NORMAL_MODELS = [
    "claude-3-5-sonnet-20241022",    # Быстрая
    "claude-3-opus-20240229"         # Мощная
]
```

### Бюджеты токенов

```python
BUDGET_MINIMAL = 500      # Простые вопросы
BUDGET_STANDARD = 1500    # По умолчанию
BUDGET_LARGE = 3000       # Сложные задачи
BUDGET_MAXIMUM = 5000     # Очень сложные задачи
```

---

## Исключения

### ValueError

Выбрасывается при:
- Отсутствии API ключа
- Неверном режиме работы
- Неверных параметрах

### Exception (общие)

Обрабатываются автоматически с fallback на normal mode.

---

## Переменные окружения

```bash
# Обязательные
PROXYAPI_KEY=your_key_here

# Опциональные (для thinking mode)
ANTHROPIC_API_KEY=your_key_here
```

---

## Форматы файлов

### История диалога (JSON)

```json
{
  "model": "gpt-3.5-turbo",
  "last_updated": "2026-03-01T21:00:00.000000",
  "messages": [
    {
      "role": "system",
      "content": "Системный промпт"
    },
    {
      "role": "user",
      "content": "Сообщение пользователя"
    },
    {
      "role": "assistant",
      "content": "Ответ ассистента"
    }
  ]
}
```
