# 🔄 Миграция на единый ProxyAPI

## Обзор изменений

Проект был обновлен для использования единого API ключа ProxyAPI для доступа к OpenAI и Claude Extended Thinking.

## Что изменилось

### До (v2.1)

```env
# Требовалось два ключа
PROXYAPI_KEY=your_proxyapi_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

```python
# Два разных подключения
client_openai = OpenAI(
    api_key=PROXYAPI_KEY,
    base_url="https://api.proxyapi.ru/openai/v1"
)

client_claude = Anthropic(
    api_key=ANTHROPIC_API_KEY  # Прямое подключение к Anthropic
)
```

### После (v2.2)

```env
# Требуется только один ключ
PROXYAPI_KEY=your_proxyapi_key_here
```

```python
# Единый ключ для обоих сервисов
client_openai = OpenAI(
    api_key=PROXYAPI_KEY,
    base_url="https://api.proxyapi.ru/openai/v1"
)

client_claude = Anthropic(
    api_key=PROXYAPI_KEY,  # Тот же ключ
    base_url="https://api.proxyapi.ru/anthropic"  # Через ProxyAPI
)
```

## Преимущества

### 1. Упрощенная конфигурация
- ✅ Один ключ вместо двух
- ✅ Меньше переменных окружения
- ✅ Проще для новых пользователей

### 2. Единая точка доступа
- ✅ Все запросы через ProxyAPI.ru
- ✅ Единое управление доступом
- ✅ Централизованный мониторинг

### 3. Упрощенная настройка
- ✅ Не нужен отдельный аккаунт Anthropic
- ✅ Не нужно получать второй ключ
- ✅ Меньше шагов при установке

### 4. Совместимость
- ✅ Полная совместимость с официальными SDK
- ✅ Те же API интерфейсы
- ✅ Прозрачная работа

## Изменения в коде

### testagent.py

**Было:**
```python
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=ANTHROPIC_API_KEY)
```

**Стало:**
```python
PROXYAPI_KEY = os.getenv("PROXYAPI_KEY")
ANTHROPIC_BASE_URL = "https://api.proxyapi.ru/anthropic"

client = Anthropic(
    api_key=PROXYAPI_KEY,
    base_url=ANTHROPIC_BASE_URL
)
```

### chat_bot.py

**Было:**
```python
def __init__(self, ..., anthropic_key=None):
    self.anthropic_key = anthropic_key or os.getenv("ANTHROPIC_API_KEY")
```

**Стало:**
```python
def __init__(self, ...):
    self.api_key = api_key  # Единый ключ для всех сервисов
```

### test_chat.py

**Было:**
```python
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

**Стало:**
```python
# Используется только API_KEY (ProxyAPI)
```

## Миграция существующих проектов

### Шаг 1: Обновите .env

**Удалите:**
```env
ANTHROPIC_API_KEY=sk-ant-...
```

**Оставьте только:**
```env
PROXYAPI_KEY=your_proxyapi_key_here
```

### Шаг 2: Обновите код

Если вы использовали прямое подключение к Anthropic:

**Было:**
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

**Стало:**
```python
from anthropic import Anthropic

client = Anthropic(
    api_key=os.getenv("PROXYAPI_KEY"),
    base_url="https://api.proxyapi.ru/anthropic"
)
```

### Шаг 3: Обновите зависимости

```bash
pip install -r requirements.txt
```

### Шаг 4: Тестирование

```bash
python test_claude_integration.py
```

## Обратная совместимость

### Для пользователей v2.1

Если у вас уже был `ANTHROPIC_API_KEY`, вы можете:

1. **Вариант 1:** Использовать ProxyAPI (рекомендуется)
   - Удалите `ANTHROPIC_API_KEY`
   - Используйте только `PROXYAPI_KEY`

2. **Вариант 2:** Временная совместимость
   ```python
   # В testagent.py можно добавить fallback
   api_key = os.getenv("PROXYAPI_KEY") or os.getenv("ANTHROPIC_API_KEY")
   ```

## Архитектура

### Новая схема подключения

```
┌─────────────────────────────────────────────────────────┐
│                    Application                          │
│                                                         │
│  ┌──────────────┐              ┌──────────────┐        │
│  │   OpenAI     │              │   Claude     │        │
│  │   Client     │              │   Client     │        │
│  └──────┬───────┘              └──────┬───────┘        │
│         │                              │                │
│         │    PROXYAPI_KEY             │                │
│         └──────────────┬───────────────┘                │
└────────────────────────┼────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    ProxyAPI.ru       │
              │                      │
              │  /openai/v1          │
              │  /anthropic          │
              └──────────┬───────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
    ┌──────────┐                 ┌──────────┐
    │ OpenAI   │                 │Anthropic │
    │   API    │                 │   API    │
    └──────────┘                 └──────────┘
```

## Конфигурация ProxyAPI

### Endpoints

- **OpenAI:** `https://api.proxyapi.ru/openai/v1`
- **Claude:** `https://api.proxyapi.ru/anthropic`

### Поддерживаемые модели

#### OpenAI через ProxyAPI
- gpt-3.5-turbo
- gpt-4
- gpt-4o
- gpt-4-turbo

#### Claude через ProxyAPI
- claude-sonnet-4-20250514 (Extended Thinking)
- claude-3-5-sonnet-20241022
- claude-3-opus-20240229

## Тестирование

### Проверка подключения

```bash
# Тест интеграции
python test_claude_integration.py

# Должно показать:
# ✓ PROXYAPI_KEY установлен
# ℹ️  Используется единый ключ для OpenAI и Claude через ProxyAPI.ru
```

### Тест OpenAI

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("PROXYAPI_KEY"),
    base_url="https://api.proxyapi.ru/openai/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Привет!"}]
)
print(response.choices[0].message.content)
```

### Тест Claude

```python
from anthropic import Anthropic

client = Anthropic(
    api_key=os.getenv("PROXYAPI_KEY"),
    base_url="https://api.proxyapi.ru/anthropic"
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Привет!"}]
)
print(response.content[0].text)
```

## FAQ

### Q: Нужен ли мне аккаунт Anthropic?
**A:** Нет! Используется только ProxyAPI.

### Q: Работает ли Extended Thinking через ProxyAPI?
**A:** Да, полностью поддерживается.

### Q: Изменилась ли стоимость?
**A:** Стоимость зависит от тарифов ProxyAPI.ru

### Q: Можно ли использовать прямое подключение к Anthropic?
**A:** Технически да, но не рекомендуется. Проект оптимизирован для ProxyAPI.

### Q: Что делать со старым ANTHROPIC_API_KEY?
**A:** Можете удалить из .env, он больше не используется.

## Troubleshooting

### Ошибка: Invalid API Key

**Проблема:**
```
anthropic.AuthenticationError: Invalid API Key
```

**Решение:**
1. Проверьте что используется `PROXYAPI_KEY`
2. Проверьте что `base_url` установлен на ProxyAPI
3. Убедитесь что ключ валидный

### Ошибка: Connection refused

**Проблема:**
```
Connection refused to api.anthropic.com
```

**Решение:**
Убедитесь что установлен `base_url`:
```python
client = Anthropic(
    api_key=PROXYAPI_KEY,
    base_url="https://api.proxyapi.ru/anthropic"  # Важно!
)
```

### Ошибка: Model not found

**Проблема:**
```
Model 'claude-sonnet-4-20250514' not found
```

**Решение:**
Проверьте доступные модели на ProxyAPI.ru

## Поддержка

Если возникли проблемы:

1. Проверьте [QUICKSTART_CLAUDE.md](QUICKSTART_CLAUDE.md)
2. Запустите `test_claude_integration.py`
3. Проверьте конфигурацию в `.env`
4. Обратитесь к документации ProxyAPI: https://proxyapi.ru/docs

## Заключение

Миграция на единый ProxyAPI упрощает:
- ✅ Конфигурацию (1 ключ вместо 2)
- ✅ Установку (меньше шагов)
- ✅ Управление (единая точка доступа)
- ✅ Мониторинг (централизованный)

**Версия:** 2.2  
**Дата:** 2026-03-01  
**Статус:** ✅ Завершено
