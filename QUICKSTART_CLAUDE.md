# 🚀 Быстрый старт с Claude Extended Thinking через ProxyAPI.ru

## За 5 минут до первого запроса

### 1️⃣ Установка (2 минуты)

```bash
# Создайте виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt
```

### 2️⃣ Настройка API ключа (1 минута)

Создайте файл `.env`:
```env
PROXYAPI_KEY=your_proxyapi_key_here
```

**Важно:** Используется единый ключ ProxyAPI для доступа к OpenAI и Claude!

**Где получить ключ:**
- ProxyAPI: https://proxyapi.ru

**Преимущества единого ProxyAPI:**
- ✅ Один ключ для всех сервисов (OpenAI + Claude)
- ✅ Единая точка доступа
- ✅ Упрощенная конфигурация
- ✅ Не нужен отдельный ключ Anthropic

### 3️⃣ Проверка (1 минута)

```bash
python test_claude_integration.py
```

Вы должны увидеть:
```
✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
```

### 4️⃣ Первый запрос (1 минута)

```bash
python testagent.py
```

Или интерактивный режим:
```bash
python test_chat.py
```

Выберите режим "1" (Thinking Mode) и введите:
```
Вы: Объясни что такое рекурсия
```

## 🎯 Что вы увидите

```
======================================================================
Модель: claude-sonnet-4-20250514
======================================================================

🧠 ПРОЦЕСС РАЗМЫШЛЕНИЯ:
----------------------------------------------------------------------
The user is asking about recursion. This is a fundamental programming
concept. I should explain it clearly with a simple example.

Key points to cover:
1. Definition - function calling itself
2. Base case - when to stop
3. Recursive case - how it calls itself
4. Simple example
----------------------------------------------------------------------

💬 ОТВЕТ:
----------------------------------------------------------------------
Рекурсия - это когда функция вызывает саму себя...
[подробное объяснение]
----------------------------------------------------------------------

📊 СТАТИСТИКА:
  • Входные токены: 45
  • Выходные токены: 120
  • Всего токенов: 165
======================================================================
```

## 💻 Использование в коде

### Вариант 1: Простейший

```python
from testagent import chat_with_thinking_model

result = chat_with_thinking_model("Привет!")
print(result['response'])
```

### Вариант 2: С форматированием

```python
from testagent import chat_with_thinking_model, format_thinking_response

result = chat_with_thinking_model("Объясни квантовую физику")
print(format_thinking_response(result))
```

### Вариант 3: Через ChatBot

```python
from chat_bot import ChatBot

bot = ChatBot(mode="thinking")
result = bot.chat("Решите уравнение: 2x + 5 = 15")

print("Размышление:", result['thinking'])
print("Ответ:", result['response'])
```

### Вариант 4: С настройкой бюджета

```python
from testagent import chat_with_thinking_model

# Для сложных задач - больше токенов
result = chat_with_thinking_model(
    "Докажите теорему Пифагора",
    thinking_budget=3000
)
```

## 🔄 Переключение режимов

### В интерактивном чате

```bash
python test_chat.py
```

Во время работы введите команду `режим`:
```
Вы: режим

🔄 Смена режима:
1. Thinking Mode (Claude)
2. Normal Mode (OpenAI)
Выберите (1/2): 2

✓ Переключено на Normal Mode (OpenAI gpt-3.5-turbo)
```

### В коде

```python
from chat_bot import ChatBot

bot = ChatBot(mode="thinking")
bot.chat("Сложный вопрос")  # Использует Claude

bot.set_mode("normal")
bot.chat("Простой вопрос")  # Использует OpenAI
```

## 📊 Когда использовать какой режим

### Thinking Mode (Claude) 🧠

**Используйте для:**
- ✅ Математических задач
- ✅ Логических головоломок
- ✅ Анализа кода
- ✅ Сложных объяснений
- ✅ Принятия решений
- ✅ Когда нужно видеть процесс мышления

**Пример:**
```python
result = chat_with_thinking_model(
    "Найдите ошибку в этом коде: [код]"
)
# Увидите как модель анализирует код
```

### Normal Mode (OpenAI) ⚡

**Используйте для:**
- ✅ Простых вопросов
- ✅ Приветствий
- ✅ Быстрых ответов
- ✅ Генерации текста
- ✅ Когда скорость важнее

**Пример:**
```python
response = generate_response("Привет!", mode="normal")
# Быстрый ответ без размышлений
```

## ⚙️ Настройка бюджета токенов

```python
# Минимальный (500) - простые вопросы
result = chat_with_thinking_model("Привет", thinking_budget=500)

# Стандартный (1500) - обычные задачи [По умолчанию]
result = chat_with_thinking_model("Объясни X", thinking_budget=1500)

# Большой (3000) - сложные задачи
result = chat_with_thinking_model("Докажите теорему", thinking_budget=3000)

# Максимальный (5000) - очень сложные задачи
result = chat_with_thinking_model("Сложный анализ", thinking_budget=5000)
```

## 🎓 Примеры задач

### Математика

```python
result = chat_with_thinking_model(
    "Решите систему уравнений: x+y=10, x-y=2",
    thinking_budget=2000
)
```

### Программирование

```python
result = chat_with_thinking_model(
    "Объясни разницу между async/await и threading в Python",
    thinking_budget=2500
)
```

### Логика

```python
result = chat_with_thinking_model(
    "Если все A это B, и все B это C, то все A это C?",
    thinking_budget=1500
)
```

### Анализ

```python
result = chat_with_thinking_model(
    "Проанализируй плюсы и минусы микросервисной архитектуры",
    thinking_budget=3000
)
```

## 🐛 Troubleshooting

### Проблема: Claude недоступен

```
⚠️  testagent.py не найден
```

**Решение:**
```bash
# Проверьте что файл существует
ls testagent.py

# Проверьте установку anthropic
pip install anthropic
```

### Проблема: Ошибка API ключа

```
⚠️  PROXYAPI_KEY не установлен
```

**Решение:**
1. Создайте `.env` файл
2. Добавьте `PROXYAPI_KEY=your_key_here`
3. Получите ключ на https://proxyapi.ru

**Примечание:** Используется единый ключ для OpenAI и Claude!

### Проблема: Автоматическое переключение на Normal Mode

```
⚠️  Ошибка в режиме thinking
Переключаюсь на обычный режим...
```

**Причины:**
- Неверный API ключ
- Превышен лимит
- Проблемы с сетью

**Решение:**
- Проверьте ключ в `.env`
- Проверьте доступ к Claude через ProxyAPI на https://proxyapi.ru
- Проверьте интернет

## 📚 Дополнительные ресурсы

- [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md) - Полное руководство
- [EXAMPLES_CLAUDE.md](EXAMPLES_CLAUDE.md) - Больше примеров
- [API_REFERENCE.md](API_REFERENCE.md) - Справочник по API

## ✅ Чеклист

- [ ] Установлены зависимости
- [ ] Создан `.env` с ключами
- [ ] Пройден `test_claude_integration.py`
- [ ] Запущен `testagent.py`
- [ ] Попробован интерактивный режим
- [ ] Протестированы оба режима
- [ ] Изучены примеры

## 🎉 Готово!

Теперь вы можете:
- ✅ Использовать думающую модель Claude
- ✅ Видеть процесс размышления
- ✅ Переключаться между режимами
- ✅ Настраивать бюджет токенов
- ✅ Интегрировать в свои проекты

**Следующий шаг:** Изучите [EXAMPLES_CLAUDE.md](EXAMPLES_CLAUDE.md) для продвинутых примеров!
