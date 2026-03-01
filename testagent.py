"""
Интеграция с Claude Extended Thinking API от Anthropic через ProxyAPI.ru
Поддержка "думающей" модели с расширенным рассуждением
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Конфигурация через ProxyAPI.ru
PROXYAPI_KEY = os.getenv("PROXYAPI_KEY", "your_proxyapi_key_here")
ANTHROPIC_BASE_URL = "https://api.proxyapi.ru/anthropic"
DEFAULT_MODEL = "claude-sonnet-4-20250514"  # Думающая модель
DEFAULT_THINKING_BUDGET = 1500  # Бюджет токенов для размышлений


def chat_with_thinking_model(
    user_message,
    conversation_history=None,
    model=DEFAULT_MODEL,
    thinking_budget=DEFAULT_THINKING_BUDGET,
    system_prompt=None,
    api_key=None,
    timeout=60
):
    """
    Взаимодействие с думающей моделью Claude от Anthropic через ProxyAPI.ru
    
    Args:
        user_message: Сообщение пользователя
        conversation_history: История диалога (список словарей с role/content)
        model: Модель для использования (по умолчанию думающая)
        thinking_budget: Бюджет токенов для размышлений (default=1500)
        system_prompt: Системный промпт
        api_key: API ключ ProxyAPI (если None, берется из переменной окружения)
        timeout: Таймаут запроса в секундах (default=60)
    
    Returns:
        dict: {
            'response': текст ответа,
            'thinking': процесс размышления (если есть),
            'usage': статистика использования токенов,
            'full_message': полный объект ответа
        }
    """
    # Используем единый ключ ProxyAPI для всех сервисов
    api_key = api_key or PROXYAPI_KEY
    
    # Инициализация клиента с ProxyAPI.ru
    client = Anthropic(
        api_key=api_key,
        base_url=ANTHROPIC_BASE_URL,
        timeout=timeout
    )
    
    # Подготовка истории сообщений
    if conversation_history is None:
        conversation_history = []
    
    # Добавляем текущее сообщение пользователя
    messages = conversation_history + [{"role": "user", "content": user_message}]
    
    # Параметры запроса
    request_params = {
        "model": model,
        "max_tokens": 4096,
        "messages": messages
    }
    
    # Добавляем системный промпт если есть
    if system_prompt:
        request_params["system"] = system_prompt
    
    # Добавляем thinking для думающих моделей
    if "sonnet-4" in model.lower() or "thinking" in model.lower():
        request_params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget
        }
    
    # Отправляем запрос
    response = client.messages.create(**request_params)
    
    # Извлекаем данные из ответа
    thinking_text = None
    response_text = ""
    
    for block in response.content:
        if block.type == "thinking":
            thinking_text = block.thinking
        elif block.type == "text":
            response_text += block.text
    
    # Формируем результат
    result = {
        'response': response_text.strip(),
        'thinking': thinking_text,
        'usage': {
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens,
            'total_tokens': response.usage.input_tokens + response.usage.output_tokens
        },
        'full_message': response,
        'model': response.model,
        'stop_reason': response.stop_reason
    }
    
    return result


def format_thinking_response(result):
    """
    Красивое форматирование ответа с процессом размышления
    
    Args:
        result: Результат от chat_with_thinking_model
    
    Returns:
        str: Отформатированный текст
    """
    output = []
    output.append("=" * 70)
    output.append(f"Модель: {result['model']}")
    output.append("=" * 70)
    
    if result['thinking']:
        output.append("\n🧠 ПРОЦЕСС РАЗМЫШЛЕНИЯ:")
        output.append("-" * 70)
        output.append(result['thinking'])
        output.append("-" * 70)
    
    output.append("\n💬 ОТВЕТ:")
    output.append("-" * 70)
    output.append(result['response'])
    output.append("-" * 70)
    
    output.append(f"\n📊 СТАТИСТИКА:")
    output.append(f"  • Входные токены: {result['usage']['input_tokens']}")
    output.append(f"  • Выходные токены: {result['usage']['output_tokens']}")
    output.append(f"  • Всего токенов: {result['usage']['total_tokens']}")
    output.append(f"  • Причина остановки: {result['stop_reason']}")
    output.append("=" * 70)
    
    return "\n".join(output)


# Тестирование
if __name__ == "__main__":
    print("Тест думающей модели Claude от Anthropic через ProxyAPI.ru")
    print("=" * 70)
    
    if PROXYAPI_KEY == "your_proxyapi_key_here":
        print("⚠️  ВНИМАНИЕ: Установите PROXYAPI_KEY в .env файле")
        print("Получить ключ: https://proxyapi.ru")
    else:
        try:
            # Тест 1: Простой вопрос
            print("\nТест 1: Простой вопрос")
            result = chat_with_thinking_model(
                "Привет! Как дела?",
                system_prompt="Ты дружелюбный помощник."
            )
            print(format_thinking_response(result))
            
            # Тест 2: Сложная задача требующая размышления
            print("\n\nТест 2: Задача требующая размышления")
            result = chat_with_thinking_model(
                "Объясни разницу между async/await и threading в Python",
                thinking_budget=2000
            )
            print(format_thinking_response(result))
            
        except Exception as e:
            print(f"Ошибка: {e}")
            print("\nПроверьте:")
            print("1. PROXYAPI_KEY установлен в .env")
            print("2. У вас есть доступ к Anthropic через ProxyAPI")
            print("3. Интернет соединение работает")
