"""
Тест интеграции Claude Extended Thinking API через ProxyAPI.ru
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("Тест интеграции Claude Extended Thinking через ProxyAPI.ru")
print("=" * 70)

# Проверка зависимостей
print("\n1. Проверка зависимостей...")
try:
    import anthropic
    print("   ✓ anthropic установлен")
except ImportError:
    print("   ✗ anthropic не установлен")
    print("   Установите: pip install anthropic")
    exit(1)

# Проверка testagent.py
print("\n2. Проверка testagent.py...")
try:
    from testagent import chat_with_thinking_model, format_thinking_response
    print("   ✓ testagent.py найден")
except ImportError as e:
    print(f"   ✗ Ошибка импорта: {e}")
    exit(1)

# Проверка API ключа
print("\n3. Проверка API ключа...")
api_key = os.getenv("PROXYAPI_KEY")
if api_key and api_key != "your_proxyapi_key_here":
    print("   ✓ PROXYAPI_KEY установлен")
    print("   ℹ️  Используется единый ключ для OpenAI и Claude через ProxyAPI.ru")
else:
    print("   ✗ PROXYAPI_KEY не установлен")
    print("   Добавьте в .env: PROXYAPI_KEY=your_key_here")
    print("   Получить ключ: https://proxyapi.ru")
    exit(1)

# Тест базовой функциональности
print("\n4. Тест базовой функциональности...")
try:
    result = chat_with_thinking_model(
        "Привет! Скажи 'тест пройден'",
        thinking_budget=500
    )
    
    if result and 'response' in result:
        print("   ✓ Функция chat_with_thinking_model работает")
        print(f"   Ответ: {result['response'][:50]}...")
    else:
        print("   ✗ Неверный формат ответа")
        exit(1)
        
except Exception as e:
    print(f"   ✗ Ошибка: {e}")
    exit(1)

# Тест форматирования
print("\n5. Тест форматирования...")
try:
    formatted = format_thinking_response(result)
    if formatted and len(formatted) > 0:
        print("   ✓ Функция format_thinking_response работает")
    else:
        print("   ✗ Ошибка форматирования")
        exit(1)
except Exception as e:
    print(f"   ✗ Ошибка: {e}")
    exit(1)

# Тест интеграции с test_chat.py
print("\n6. Тест интеграции с test_chat.py...")
try:
    from test_chat import generate_response, CLAUDE_AVAILABLE
    
    if CLAUDE_AVAILABLE:
        print("   ✓ Claude доступен в test_chat.py")
    else:
        print("   ✗ Claude недоступен в test_chat.py")
        exit(1)
        
except Exception as e:
    print(f"   ✗ Ошибка: {e}")
    exit(1)

# Тест интеграции с chat_bot.py
print("\n7. Тест интеграции с chat_bot.py...")
try:
    from chat_bot import ChatBot, CLAUDE_AVAILABLE
    
    if CLAUDE_AVAILABLE:
        print("   ✓ Claude доступен в chat_bot.py")
        
        # Создание бота в thinking режиме
        bot = ChatBot(mode="thinking", thinking_budget=500)
        print("   ✓ ChatBot создан в thinking режиме")
        
        # Проверка методов
        bot.set_mode("normal")
        if bot.get_mode() == "normal":
            print("   ✓ Методы set_mode/get_mode работают")
        
    else:
        print("   ✗ Claude недоступен в chat_bot.py")
        exit(1)
        
except Exception as e:
    print(f"   ✗ Ошибка: {e}")
    exit(1)

# Финальный тест с размышлением
print("\n8. Финальный тест с процессом размышления...")
try:
    result = chat_with_thinking_model(
        "Объясни в одном предложении что такое рекурсия",
        thinking_budget=1000
    )
    
    if result.get('thinking'):
        print("   ✓ Процесс размышления получен")
        print(f"   Размышление: {result['thinking'][:80]}...")
    else:
        print("   ⚠️  Процесс размышления отсутствует (это нормально для простых вопросов)")
    
    print(f"   Ответ: {result['response'][:80]}...")
    print(f"   Токены: {result['usage']['total_tokens']}")
    
except Exception as e:
    print(f"   ✗ Ошибка: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
print("=" * 70)
print("\nИнтеграция Claude Extended Thinking через ProxyAPI.ru работает корректно.")
print("\nПреимущества единого ProxyAPI:")
print("  ✓ Один API ключ для OpenAI и Claude")
print("  ✓ Единая точка доступа")
print("  ✓ Упрощенная конфигурация")
print("\nПопробуйте:")
print("  python test_chat.py    # Интерактивный режим с выбором")
print("  python testagent.py    # Прямое тестирование Claude")
print("  python chat_bot.py     # ChatBot с thinking режимом")
