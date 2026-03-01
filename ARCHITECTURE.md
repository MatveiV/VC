# 🏗️ Архитектура проекта

## Обзор системы

Проект представляет собой многорежимный чат-бот с поддержкой двух AI провайдеров:
- **OpenAI** через ProxyAPI.ru (Normal Mode)
- **Anthropic Claude** с Extended Thinking (Thinking Mode)

## Архитектурная диаграмма

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ chat_bot.py  │  │test_chat.py  │  │testagent.py  │         │
│  │ (Class API)  │  │(Functional)  │  │(Claude Only) │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Mode Selection & Routing                    │  │
│  │  • Thinking Mode → Claude Extended Thinking              │  │
│  │  • Normal Mode → OpenAI via ProxyAPI                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Context Management                          │  │
│  │  • Conversation history                                  │  │
│  │  • Auto-save/load from JSON                              │  │
│  │  • System prompts                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │                                    │
          ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│   OPENAI PROVIDER    │          │  ANTHROPIC PROVIDER  │
│                      │          │                      │
│  ┌────────────────┐  │          │  ┌────────────────┐  │
│  │ OpenAI Client │  │          │  │Anthropic Client│  │
│  │   (SDK)       │  │          │  │   (SDK)        │  │
│  └────────┬───────┘  │          │  └────────┬───────┘  │
│           │          │          │           │          │
│           ▼          │          │           ▼          │
│  ┌────────────────┐  │          │  ┌────────────────┐  │
│  │  ProxyAPI.ru  │  │          │  │ Claude API     │  │
│  │  Base URL     │  │          │  │ Extended       │  │
│  └────────────────┘  │          │  │ Thinking       │  │
│                      │          │  └────────────────┘  │
└──────────────────────┘          └──────────────────────┘
          │                                    │
          ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│   OpenAI API         │          │   Anthropic API      │
│   (External)         │          │   (External)         │
└──────────────────────┘          └──────────────────────┘
```

## Компоненты системы

### 1. User Interface Layer

#### chat_bot.py (Class-based API)
```python
class ChatBot:
    - __init__()          # Инициализация с выбором режима
    - chat()              # Отправка сообщения
    - set_mode()          # Переключение режима
    - get_mode()          # Получение текущего режима
    - set_system_prompt() # Настройка поведения
    - save_history()      # Сохранение контекста
    - load_history()      # Загрузка контекста
    - reset_conversation()# Очистка истории
```

**Особенности:**
- Объектно-ориентированный подход
- Инкапсуляция состояния
- Автоматическое управление историей
- Поддержка обоих режимов

#### test_chat.py (Functional API)
```python
Functions:
    - generate_response()    # Универсальная генерация
    - chat_loop()            # Интерактивный режим
    - add_message()          # Добавление в историю
    - save_history()         # Сохранение
    - load_history()         # Загрузка
    - reset_conversation()   # Очистка
```

**Особенности:**
- Функциональный подход
- Глобальное состояние
- Простота использования
- Интерактивный режим с выбором

#### testagent.py (Claude-specific)
```python
Functions:
    - chat_with_thinking_model()  # Прямой доступ к Claude
    - format_thinking_response()  # Форматирование вывода
```

**Особенности:**
- Специализация на Claude
- Прямой доступ к Extended Thinking
- Независимый модуль
- Можно использовать отдельно

### 2. Business Logic Layer

#### Mode Selection & Routing

```python
if mode == "thinking" and CLAUDE_AVAILABLE:
    # Route to Anthropic Claude
    result = chat_with_thinking_model(...)
    return result  # dict with thinking + response
else:
    # Route to OpenAI via ProxyAPI
    response = client.chat.completions.create(...)
    return response.choices[0].message.content  # str
```

**Логика выбора:**
1. Проверка режима (thinking/normal)
2. Проверка доступности Claude
3. Маршрутизация к соответствующему провайдеру
4. Обработка ошибок с fallback

#### Context Management

```python
conversation_history = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
```

**Функции:**
- Хранение истории диалога
- Автоматическое сохранение в JSON
- Загрузка при инициализации
- Совместимость между режимами

### 3. Provider Layer

#### OpenAI Provider

```python
client = OpenAI(
    api_key=PROXYAPI_KEY,
    base_url="https://api.proxyapi.ru/openai/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=conversation_history
)
```

**Характеристики:**
- Использует ProxyAPI.ru как прокси
- Стандартный OpenAI SDK
- Быстрые ответы
- Дешевле

#### Anthropic Provider

```python
client = Anthropic(api_key=ANTHROPIC_API_KEY)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=conversation_history,
    thinking={
        "type": "enabled",
        "budget_tokens": 1500
    }
)
```

**Характеристики:**
- Прямое подключение к Anthropic
- Extended Thinking API
- Процесс размышления
- Настраиваемый бюджет

## Потоки данных

### Thinking Mode Flow

```
User Input
    ↓
[chat_bot.py / test_chat.py]
    ↓
Mode Check (thinking?)
    ↓
[testagent.py]
    ↓
chat_with_thinking_model()
    ↓
Anthropic Client
    ↓
Claude API (Extended Thinking)
    ↓
Response with thinking + text
    ↓
Format & Display
    ↓
Save to History
    ↓
Return to User
```

### Normal Mode Flow

```
User Input
    ↓
[chat_bot.py / test_chat.py]
    ↓
Mode Check (normal?)
    ↓
OpenAI Client
    ↓
ProxyAPI.ru
    ↓
OpenAI API
    ↓
Response (text only)
    ↓
Save to History
    ↓
Return to User
```

## Форматы данных

### Thinking Mode Response

```python
{
    'response': str,           # Финальный ответ
    'thinking': str | None,    # Процесс размышления
    'usage': {
        'input_tokens': int,
        'output_tokens': int,
        'total_tokens': int
    },
    'full_message': Message,   # Полный объект
    'model': str,              # Модель
    'stop_reason': str         # Причина остановки
}
```

### Normal Mode Response

```python
str  # Просто текст ответа
```

### History Format (JSON)

```json
{
  "model": "gpt-3.5-turbo",
  "last_updated": "2026-03-01T21:00:00.000000",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## Конфигурация

### Environment Variables

```env
# OpenAI через ProxyAPI (обязательно)
PROXYAPI_KEY=sk-...

# Anthropic Claude (опционально, для thinking mode)
ANTHROPIC_API_KEY=sk-ant-...
```

### Application Config

```python
# OpenAI
MODEL = "gpt-3.5-turbo"
BASE_URL = "https://api.proxyapi.ru/openai/v1"

# Claude
CLAUDE_MODEL = "claude-sonnet-4-20250514"
THINKING_BUDGET = 1500

# Mode
CURRENT_MODE = "thinking"  # или "normal"
```

## Обработка ошибок

### Error Handling Strategy

```python
try:
    # Попытка использовать выбранный режим
    if mode == "thinking":
        result = chat_with_thinking_model(...)
except Exception as e:
    # Логирование ошибки
    print(f"⚠️  Ошибка в режиме thinking: {e}")
    
    # Автоматический fallback на normal mode
    print("Переключаюсь на обычный режим...")
    result = openai_client.chat.completions.create(...)
```

### Error Types

1. **API Key Missing** → ValueError при инициализации
2. **Network Error** → Retry или fallback
3. **Rate Limit** → Fallback на другой режим
4. **Invalid Response** → Обработка и повтор

## Масштабируемость

### Horizontal Scaling

```
Load Balancer
    ↓
┌────────────┬────────────┬────────────┐
│ Instance 1 │ Instance 2 │ Instance 3 │
└────────────┴────────────┴────────────┘
    ↓              ↓              ↓
┌────────────────────────────────────┐
│      Shared History Storage        │
│      (Redis / Database)            │
└────────────────────────────────────┘
```

### Vertical Scaling

- Увеличение `thinking_budget` для сложных задач
- Использование более мощных моделей
- Кэширование частых запросов

## Безопасность

### API Keys

- Хранятся в `.env` (не коммитятся)
- Загружаются через `python-dotenv`
- Никогда не логируются

### Input Validation

```python
if not api_key:
    raise ValueError("API ключ не найден")

if mode not in ["thinking", "normal"]:
    raise ValueError("Неверный режим")
```

### Rate Limiting

- Автоматический fallback при превышении лимитов
- Контроль бюджета токенов
- Мониторинг использования

## Тестирование

### Unit Tests

- `test_claude_integration.py` - интеграция с Claude
- `test_persistence.py` - сохранение контекста
- `test_save_load.py` - работа с файлами

### Integration Tests

- `quick_test.py` - базовая функциональность
- `testagent.py` - прямое тестирование Claude

### Manual Testing

- `chat_bot.py` - интерактивный режим
- `test_chat.py` - функциональный режим
- `demo_persistence.py` - демонстрация

## Производительность

### Thinking Mode

- **Latency**: 2-5 секунд (зависит от thinking_budget)
- **Throughput**: ~10-20 запросов/минуту
- **Cost**: ~$0.003-0.015 за запрос

### Normal Mode

- **Latency**: 0.5-2 секунды
- **Throughput**: ~30-60 запросов/минуту
- **Cost**: ~$0.0001-0.001 за запрос

## Мониторинг

### Metrics to Track

```python
{
    'mode': 'thinking',
    'tokens_used': 165,
    'thinking_tokens': 45,
    'response_time': 3.2,
    'success': True,
    'model': 'claude-sonnet-4-20250514'
}
```

### Logging

```python
print(f"✓ Загружена история из {history_file}")
print(f"⚠️  Ошибка в режиме thinking: {error}")
print(f"📊 Токены: {usage['total_tokens']}")
```

## Будущие улучшения

### Planned Features

1. **Streaming responses** - потоковая передача ответов
2. **Multi-session support** - несколько диалогов
3. **Web interface** - веб-интерфейс
4. **Voice I/O** - голосовой ввод/вывод
5. **Image support** - работа с изображениями (GPT-4 Vision)
6. **Plugin system** - система плагинов
7. **Analytics dashboard** - дашборд аналитики

### Architecture Evolution

```
Current: Monolithic
    ↓
Next: Microservices
    ↓
Future: Serverless + Edge
```

## Заключение

Архитектура проекта обеспечивает:
- ✅ Гибкость (два режима работы)
- ✅ Надежность (fallback механизмы)
- ✅ Масштабируемость (легко добавить новые провайдеры)
- ✅ Простоту (понятный API)
- ✅ Расширяемость (модульная структура)
