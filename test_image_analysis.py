"""
Тест анализа изображений PNG
"""

from chat_bot import ChatBot
import os

print("=" * 70)
print("ТЕСТ АНАЛИЗА ИЗОБРАЖЕНИЙ PNG")
print("=" * 70)

# Проверка наличия изображения
print("\n1. Проверка файла изображения...")
image_path = input("Введите путь к PNG изображению (или Enter для Claude.png): ").strip()

if not image_path:
    image_path = "Claude.png"

if not os.path.exists(image_path):
    print(f"❌ Файл не найден: {image_path}")
    print("\nСоздайте тестовое изображение или укажите существующий файл.")
    exit(1)

print(f"✓ Файл найден: {image_path}")
print(f"  Размер: {os.path.getsize(image_path)} байт")

# Проверка моделей с vision
print("\n2. Доступные модели с Vision API:")
from models_config import get_vision_models

vision_models = get_vision_models()
print("\nOpenAI модели:")
for model_id, info in vision_models.items():
    if info.provider == "openai":
        print(f"  - {info.name} ({model_id})")

print("\nClaude модели:")
for model_id, info in vision_models.items():
    if info.provider == "claude":
        print(f"  - {info.name} ({model_id})")
        print(f"    ⚠️  Claude через ProxyAPI пока не поддерживает изображения")

# Выбор модели
print("\n3. Выбор модели для анализа:")
print("1. gpt-4o (рекомендуется)")
print("2. gpt-4-turbo")

choice = input("\nВыберите модель (1/2, Enter=1): ").strip()
model = "gpt-4o" if choice != "2" else "gpt-4-turbo"

print(f"\n✓ Выбрана модель: {model}")

# Создание бота
print("\n4. Инициализация ChatBot...")
bot = ChatBot(model=model, mode="normal")
print("✓ ChatBot готов к работе")

# Тест 1: Общий анализ
print("\n" + "=" * 70)
print("ТЕСТ 1: ОБЩИЙ АНАЛИЗ ИЗОБРАЖЕНИЯ")
print("=" * 70)

try:
    response = bot.chat(
        "Опиши детально что изображено на этой картинке",
        file_path=image_path
    )
    print("\n💬 ОТВЕТ:")
    print(response)
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Тест 2: Извлечение текста
print("\n" + "=" * 70)
print("ТЕСТ 2: ИЗВЛЕЧЕНИЕ ТЕКСТА (OCR)")
print("=" * 70)

try:
    response = bot.chat(
        "Есть ли текст на этом изображении? Если да, извлеки весь текст",
        file_path=image_path
    )
    print("\n💬 ОТВЕТ:")
    print(response)
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Тест 3: Пользовательский вопрос
print("\n" + "=" * 70)
print("ТЕСТ 3: ПОЛЬЗОВАТЕЛЬСКИЙ ВОПРОС")
print("=" * 70)

custom_question = input("\nВаш вопрос об изображении (Enter для пропуска): ").strip()

if custom_question:
    try:
        response = bot.chat(
            custom_question,
            file_path=image_path
        )
        print("\n💬 ОТВЕТ:")
        print(response)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
else:
    print("Пропущено")

# Итоги
print("\n" + "=" * 70)
print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 70)

print("\n📋 ИТОГИ:")
print(f"  ✓ Изображение: {image_path}")
print(f"  ✓ Модель: {model}")
print(f"  ✓ Тестов выполнено: 2-3")

print("\n💡 ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ:")
print("  • Анализ UI/UX дизайна")
print("  • Извлечение текста (OCR)")
print("  • Распознавание объектов")
print("  • Анализ графиков и диаграмм")
print("  • Проверка документов")

print("\n📚 Подробнее: IMAGE_ANALYSIS_GUIDE.md")
print("=" * 70)
