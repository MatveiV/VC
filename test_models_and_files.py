"""
Тест функциональности выбора моделей и работы с файлами
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("ТЕСТ: Выбор моделей и работа с файлами")
print("=" * 70)

# Тест 1: Импорт модулей
print("\n1. Проверка импорта модулей...")
try:
    from models_config import get_model_info, list_models, get_vision_models
    print("   ✓ models_config.py импортирован")
except ImportError as e:
    print(f"   ✗ Ошибка импорта models_config: {e}")
    exit(1)

try:
    from file_handler import load_file, get_supported_formats
    print("   ✓ file_handler.py импортирован")
except ImportError as e:
    print(f"   ✗ Ошибка импорта file_handler: {e}")
    exit(1)

try:
    from chat_bot import ChatBot
    print("   ✓ chat_bot.py импортирован")
except ImportError as e:
    print(f"   ✗ Ошибка импорта chat_bot: {e}")
    exit(1)

# Тест 2: Конфигурация моделей
print("\n2. Проверка конфигурации моделей...")
models = list_models()
print(f"   ✓ Доступно моделей: {len(models)}")

openai_models = list_models("openai")
claude_models = list_models("claude")
print(f"   ✓ OpenAI моделей: {len(openai_models)}")
print(f"   ✓ Claude моделей: {len(claude_models)}")

vision_models = get_vision_models()
print(f"   ✓ Моделей с vision: {len(vision_models)}")

# Тест 3: Информация о моделях
print("\n3. Проверка информации о моделях...")
test_models = ["gpt-4o", "gpt-3.5-turbo", "claude-sonnet-4-20250514"]
for model_id in test_models:
    info = get_model_info(model_id)
    if info:
        print(f"   ✓ {info.name}")
        print(f"     - Провайдер: {info.provider}")
        print(f"     - Vision: {info.supports_vision}")
        print(f"     - Thinking: {info.supports_thinking}")
    else:
        print(f"   ✗ Модель {model_id} не найдена")

# Тест 4: Поддерживаемые форматы файлов
print("\n4. Проверка поддерживаемых форматов...")
formats = get_supported_formats()
print(f"   ✓ Текстовых форматов: {len(formats['text'])}")
print(f"   ✓ Форматов изображений: {len(formats['image'])}")
print(f"   ✓ Форматов документов: {len(formats['document'])}")

# Тест 5: Создание тестового файла
print("\n5. Создание тестового файла...")
test_file = "test_example.txt"
with open(test_file, 'w', encoding='utf-8') as f:
    f.write("Это тестовый файл для проверки функциональности.\n")
    f.write("Он содержит несколько строк текста.\n")
    f.write("Модель должна уметь его прочитать и проанализировать.\n")
print(f"   ✓ Создан файл: {test_file}")

# Тест 6: Загрузка файла
print("\n6. Проверка загрузки файла...")
try:
    file_info = load_file(test_file)
    print(f"   ✓ Файл загружен: {file_info.name}")
    print(f"   ✓ Размер: {file_info.size} байт")
    print(f"   ✓ Тип: {file_info.mime_type}")
    print(f"   ✓ Содержимое загружено: {len(file_info.content)} символов")
except Exception as e:
    print(f"   ✗ Ошибка загрузки: {e}")

# Тест 7: Создание ChatBot с разными моделями
print("\n7. Проверка создания ChatBot...")
try:
    bot = ChatBot(model="gpt-3.5-turbo")
    print(f"   ✓ ChatBot создан с моделью: {bot.get_current_model()}")
except Exception as e:
    print(f"   ✗ Ошибка создания ChatBot: {e}")

# Тест 8: Смена модели
print("\n8. Проверка смены модели...")
try:
    bot.set_model("gpt-4o")
    print(f"   ✓ Модель изменена на: {bot.get_current_model()}")
    
    bot.set_model("claude-3-5-sonnet-20241022")
    print(f"   ✓ Модель изменена на: {bot.get_current_model()}")
except Exception as e:
    print(f"   ✗ Ошибка смены модели: {e}")

# Тест 9: Проверка API ключа
print("\n9. Проверка API ключа...")
api_key = os.getenv("PROXYAPI_KEY")
if api_key and api_key != "your_proxyapi_key_here":
    print("   ✓ PROXYAPI_KEY установлен")
else:
    print("   ⚠️  PROXYAPI_KEY не установлен (тесты с API будут пропущены)")

# Тест 10: Интеграционный тест (если есть API ключ)
if api_key and api_key != "your_proxyapi_key_here":
    print("\n10. Интеграционный тест с файлом...")
    try:
        bot = ChatBot(model="gpt-3.5-turbo")
        response = bot.chat("Кратко опиши содержимое", file_path=test_file)
        print(f"   ✓ Ответ получен: {response[:100]}...")
    except Exception as e:
        print(f"   ⚠️  Ошибка интеграционного теста: {e}")
else:
    print("\n10. Интеграционный тест пропущен (нет API ключа)")

# Очистка
print("\n11. Очистка...")
if os.path.exists(test_file):
    os.remove(test_file)
    print(f"   ✓ Удален тестовый файл: {test_file}")

print("\n" + "=" * 70)
print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
print("=" * 70)

print("\nИтоги:")
print(f"  ✓ Модулей импортировано: 3")
print(f"  ✓ Моделей доступно: {len(models)}")
print(f"  ✓ Форматов файлов поддерживается: {sum(len(v) for v in formats.values())}")
print("\nПопробуйте:")
print("  python demo_models_and_files.py  # Интерактивная демонстрация")
print("  python models_config.py          # Список всех моделей")
print("  python file_handler.py           # Список форматов файлов")
