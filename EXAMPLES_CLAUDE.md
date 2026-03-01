# 📚 Примеры использования Claude Extended Thinking

## Пример 1: Простой диалог

```python
from testagent import chat_with_thinking_model, format_thinking_response

result = chat_with_thinking_model("Привет! Как дела?")
print(format_thinking_response(result))
```

**Вывод:**
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

## Пример 2: Математическая задача

```python
result = chat_with_thinking_model(
    "Решите уравнение: 3x² - 12x + 9 = 0",
    thinking_budget=2500
)
print(format_thinking_response(result))
```

## Пример 3: Диалог с контекстом

```python
from testagent import chat_with_thinking_model

# Первое сообщение
history = []
result1 = chat_with_thinking_model(
    "Меня зовут Алексей, я программист",
    conversation_history=history
)

# Обновляем историю
history.append({"role": "user", "content": "Меня зовут Алексей, я программист"})
history.append({"role": "assistant", "content": result1['response']})

# Второе сообщение (с контекстом)
result2 = chat_with_thinking_model(
    "Как меня зовут и кем я работаю?",
    conversation_history=history
)

print(result2['response'])
# Ответ: "Вас зовут Алексей, и вы работаете программистом."
```

## Пример 4: Использование через test_chat.py

```python
from test_chat import generate_response, CURRENT_MODE

# Установка режима
CURRENT_MODE = "thinking"

# Простой запрос
result = generate_response("Объясни async/await в Python")

# Доступ к данным
print("Процесс мышления:", result['thinking'])
print("Ответ:", result['response'])
print("Токены:", result['usage']['total_tokens'])
```

## Пример 5: Через ChatBot класс

```python
from chat_bot import ChatBot

# Создание бота в thinking режиме
bot = ChatBot(
    mode="thinking",
    claude_model="claude-sonnet-4-20250514",
    thinking_budget=2000
)

bot.set_system_prompt("Ты эксперт по Python.")

# Диалог
response1 = bot.chat("Что такое декораторы?")
print(response1['response'])

response2 = bot.chat("Приведи пример")
print(response2['response'])

# Переключение режима
bot.set_mode("normal")
response3 = bot.chat("Спасибо!")
print(response3)  # Теперь просто строка
```

## Пример 6: Адаптивный бюджет

```python
def smart_chat(user_message):
    """Автоматически выбирает бюджет в зависимости от задачи"""
    
    # Определяем сложность
    if any(word in user_message.lower() for word in ['математика', 'решите', 'вычислите']):
        budget = 3000
    elif any(word in user_message.lower() for word in ['объясни', 'расскажи', 'опиши']):
        budget = 2000
    else:
        budget = 1500
    
    result = chat_with_thinking_model(
        user_message,
        thinking_budget=budget
    )
    
    return result

# Использование
result = smart_chat("Решите систему уравнений: x+y=5, x-y=1")
print(f"Использован бюджет: {result['usage']['output_tokens']} токенов")
```

## Пример 7: Сравнение режимов

```python
from test_chat import generate_response

question = "Что такое квантовая запутанность?"

# Thinking Mode
print("=== THINKING MODE ===")
result_thinking = generate_response(question, mode="thinking")
print("Процесс мышления:", result_thinking['thinking'][:200], "...")
print("Ответ:", result_thinking['response'][:200], "...")
print("Токены:", result_thinking['usage']['total_tokens'])

# Normal Mode
print("\n=== NORMAL MODE ===")
result_normal = generate_response(question, mode="normal")
print("Ответ:", result_normal[:200], "...")
```

## Пример 8: Обработка ошибок

```python
from testagent import chat_with_thinking_model

try:
    result = chat_with_thinking_model(
        "Очень длинный текст..." * 10000,  # Слишком много токенов
        thinking_budget=1000
    )
except Exception as e:
    print(f"Ошибка: {e}")
    # Fallback на более простой запрос
    result = chat_with_thinking_model(
        "Краткий вопрос",
        thinking_budget=500
    )
```

## Пример 9: Интерактивный режим с выбором

```python
from test_chat import chat_loop

# Запуск интерактивного чата
# При запуске выберите режим 1 (Thinking Mode)
chat_loop()

# В чате:
# Вы: Объясни рекурсию
# [Видите процесс размышления и ответ]
#
# Вы: режим
# [Переключаетесь на Normal Mode]
#
# Вы: Привет
# [Быстрый ответ без размышлений]
```

## Пример 10: Сохранение результатов

```python
import json
from testagent import chat_with_thinking_model

# Запрос
result = chat_with_thinking_model("Объясни теорию относительности")

# Сохранение в файл
output = {
    'question': "Объясни теорию относительности",
    'thinking': result['thinking'],
    'answer': result['response'],
    'tokens': result['usage'],
    'model': result['model']
}

with open('claude_response.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Результат сохранен в claude_response.json")
```
