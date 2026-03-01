"""
Тестовый файл для работы с Chat Completions API через ProxyAPI.ru
Поддерживает режим диалога с сохранением контекста
Интеграция с Claude Extended Thinking API от Anthropic
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Импорт функции работы с думающей моделью Claude
try:
    from testagent import chat_with_thinking_model, format_thinking_response
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("⚠️  testagent.py не найден. Думающая модель Claude недоступна.")

# Загружаем переменные окружения из .env файла
load_dotenv()

# Конфигурация ProxyAPI
API_KEY = os.getenv("PROXYAPI_KEY", "your_proxyapi_key_here")
BASE_URL = "https://api.proxyapi.ru/openai/v1"
MODEL = "gpt-3.5-turbo"
HISTORY_FILE = "test_chat_history.json"

# Конфигурация Claude через ProxyAPI
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Думающая модель
THINKING_BUDGET = 1500  # Бюджет токенов для размышлений

# Режим работы: "thinking" (Claude) или "normal" (OpenAI через ProxyAPI)
CURRENT_MODE = "thinking"  # По умолчанию думающая модель

# История диалога для сохранения контекста
conversation_history = []


def add_message(role, content):
    """Добавить сообщение в историю диалога"""
    conversation_history.append({"role": role, "content": content})


def generate_response(user_message, system_prompt=None, auto_save=True, mode=None):
    """
    Генерация ответа с сохранением контекста диалога
    Поддерживает два режима: thinking (Claude) и normal (OpenAI)
    
    Args:
        user_message: Сообщение пользователя
        system_prompt: Системный промпт (опционально, только для первого сообщения)
        auto_save: Автоматически сохранять историю после каждого сообщения
        mode: Режим работы ("thinking" или "normal", если None - использует CURRENT_MODE)
    
    Returns:
        str или dict: Ответ ассистента (str для normal, dict для thinking)
    """
    global CURRENT_MODE
    
    # Определяем режим
    active_mode = mode if mode is not None else CURRENT_MODE
    
    # Добавляем системный промпт, если это первое сообщение
    if system_prompt and len(conversation_history) == 0:
        add_message("system", system_prompt)
    
    # РЕЖИМ THINKING: Claude Extended Thinking
    if active_mode == "thinking" and CLAUDE_AVAILABLE:
        try:
            # Конвертируем историю для Claude (без system в messages)
            claude_history = []
            system_for_claude = None
            
            for msg in conversation_history:
                if msg["role"] == "system":
                    system_for_claude = msg["content"]
                else:
                    claude_history.append(msg)
            
            # Вызываем думающую модель
            result = chat_with_thinking_model(
                user_message=user_message,
                conversation_history=claude_history,
                model=CLAUDE_MODEL,
                thinking_budget=THINKING_BUDGET,
                system_prompt=system_for_claude
            )
            
            # Добавляем в историю
            add_message("user", user_message)
            add_message("assistant", result['response'])
            
            # Сохраняем историю
            if auto_save:
                save_history()
            
            return result
            
        except Exception as e:
            print(f"⚠️  Ошибка в режиме thinking: {e}")
            print("Переключаюсь на обычный режим...")
            active_mode = "normal"
    
    # РЕЖИМ NORMAL: OpenAI через ProxyAPI
    # Инициализация клиента
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    
    # Добавляем сообщение пользователя
    add_message("user", user_message)
    
    # Отправляем запрос с полной историей
    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation_history
    )
    
    # Получаем ответ
    assistant_message = response.choices[0].message.content
    
    # Добавляем ответ в историю
    add_message("assistant", assistant_message)
    
    # Автоматически сохраняем историю
    if auto_save:
        save_history()
    
    return assistant_message


def save_history():
    """Сохранить историю диалога в файл"""
    try:
        data = {
            "model": MODEL,
            "last_updated": datetime.now().isoformat(),
            "messages": conversation_history
        }
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except UnicodeEncodeError:
        # Если возникла ошибка кодировки, сохраняем с ensure_ascii=True
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении истории: {e}")


def load_history():
    """Загрузить историю диалога из файла"""
    global conversation_history
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                conversation_history = data.get("messages", [])
                print(f"✓ Загружена история из {HISTORY_FILE} ({len(conversation_history)} сообщений)")
                if data.get("last_updated"):
                    print(f"  Последнее обновление: {data['last_updated']}\n")
    except Exception as e:
        print(f"Ошибка при загрузке истории: {e}")
        conversation_history = []


def reset_conversation():
    """Очистить историю диалога"""
    global conversation_history
    conversation_history = []
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


def chat_loop():
    """Запуск интерактивного диалога"""
    global CURRENT_MODE
    
    print("=" * 70)
    print("Тестовый чат-бот с ProxyAPI.ru и Claude Extended Thinking")
    print("=" * 70)
    
    # Выбор режима работы
    print("\n🤖 ВЫБОР РЕЖИМА РАБОТЫ:")
    print("1. Thinking Mode (Claude Extended Thinking) - думающая модель [По умолчанию]")
    print("2. Normal Mode (OpenAI через ProxyAPI) - обычная модель")
    
    choice = input("\nВыберите режим (1/2, Enter=1): ").strip()
    
    if choice == "2":
        CURRENT_MODE = "normal"
        print(f"\n✓ Выбран режим: Normal Mode (OpenAI {MODEL})")
    else:
        CURRENT_MODE = "thinking"
        if CLAUDE_AVAILABLE and ANTHROPIC_API_KEY != "your_anthropic_key_here":
            print(f"\n✓ Выбран режим: Thinking Mode (Claude {CLAUDE_MODEL})")
            print(f"  Бюджет токенов для размышлений: {THINKING_BUDGET}")
        else:
            print("\n⚠️  Claude недоступен. Переключаюсь на Normal Mode.")
            CURRENT_MODE = "normal"
    
    print("\nКоманды: 'выход' - завершить, 'сброс' - очистить историю, 'режим' - сменить режим")
    print(f"История автоматически сохраняется в {HISTORY_FILE}\n")
    
    # Загружаем предыдущую историю
    load_history()
    
    # Устанавливаем системный промпт, если история пустая
    system_prompt = "Ты дружелюбный помощник, который отвечает кратко и по делу."
    
    while True:
        user_input = input("Вы: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['выход', 'exit', 'quit']:
            print("До свидания!")
            break
        
        if user_input.lower() in ['сброс', 'reset']:
            reset_conversation()
            print("✓ История диалога очищена\n")
            continue
        
        if user_input.lower() in ['режим', 'mode']:
            print("\n🔄 Смена режима:")
            print("1. Thinking Mode (Claude)")
            print("2. Normal Mode (OpenAI)")
            mode_choice = input("Выберите (1/2): ").strip()
            
            if mode_choice == "2":
                CURRENT_MODE = "normal"
                print(f"✓ Переключено на Normal Mode (OpenAI {MODEL})\n")
            else:
                CURRENT_MODE = "thinking"
                print(f"✓ Переключено на Thinking Mode (Claude {CLAUDE_MODEL})\n")
            continue
        
        try:
            # Генерируем ответ
            response = generate_response(
                user_input,
                system_prompt=system_prompt if len(conversation_history) == 0 else None
            )
            
            # Форматируем вывод в зависимости от режима
            if CURRENT_MODE == "thinking" and isinstance(response, dict):
                print("\n" + format_thinking_response(response) + "\n")
            else:
                # Обычный режим или строковый ответ
                response_text = response if isinstance(response, str) else response.get('response', str(response))
                print(f"Бот: {response_text}\n")
                
        except Exception as e:
            print(f"Ошибка: {e}\n")


# Тестовые функции
def test_simple_message():
    """Тест простого сообщения"""
    print("\n--- Тест 1: Простое сообщение ---")
    reset_conversation()
    response = generate_response("Привет! Как дела?")
    print(f"Ответ: {response}")


def test_context_memory():
    """Тест сохранения контекста"""
    print("\n--- Тест 2: Сохранение контекста ---")
    reset_conversation()
    
    response1 = generate_response("Меня зовут Алексей")
    print(f"Ответ 1: {response1}")
    
    response2 = generate_response("Как меня зовут?")
    print(f"Ответ 2: {response2}")


def test_system_prompt():
    """Тест с системным промптом"""
    print("\n--- Тест 3: Системный промпт ---")
    reset_conversation()
    
    response = generate_response(
        "Расскажи про Python",
        system_prompt="Ты эксперт по программированию. Отвечай очень кратко, максимум 2 предложения."
    )
    print(f"Ответ: {response}")


if __name__ == "__main__":
    # Проверяем наличие API ключа
    if API_KEY == "your_proxyapi_key_here":
        print("ВНИМАНИЕ: Установите API ключ от ProxyAPI в переменной окружения PROXYAPI_KEY")
        print("или измените значение API_KEY в файле test_chat.py")
        print("Получить ключ можно на https://proxyapi.ru\n")
    
    # Выбор режима
    print("Выберите режим:")
    print("1 - Интерактивный чат")
    print("2 - Запустить тесты")
    
    choice = input("\nВаш выбор (1 или 2): ").strip()
    
    if choice == "1":
        chat_loop()
    elif choice == "2":
        test_simple_message()
        test_context_memory()
        test_system_prompt()
        print("\n--- Все тесты завершены ---")
    else:
        print("Неверный выбор. Запускаю интерактивный чат...")
        chat_loop()
