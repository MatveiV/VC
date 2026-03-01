"""
Демонстрация работы с различными моделями и файлами
"""

from chat_bot import ChatBot
from models_config import print_models_table, get_vision_models
from file_handler import print_supported_formats
import os

print("=" * 70)
print("ДЕМОНСТРАЦИЯ: Выбор моделей и работа с файлами")
print("=" * 70)

# Показываем доступные модели
print("\n1️⃣  ДОСТУПНЫЕ МОДЕЛИ")
print_models_table()

# Показываем поддерживаемые форматы файлов
print("\n2️⃣  ПОДДЕРЖИВАЕМЫЕ ФОРМАТЫ ФАЙЛОВ")
print_supported_formats()

# Интерактивный выбор
print("\n3️⃣  ИНТЕРАКТИВНЫЙ РЕЖИМ")
print("=" * 70)

# Выбор модели
print("\nВыберите модель:")
print("1. GPT-4o (OpenAI, с vision)")
print("2. GPT-3.5 Turbo (OpenAI, быстрая)")
print("3. Claude Sonnet 4 (Extended Thinking)")
print("4. Claude 3.5 Sonnet (быстрая, с vision)")
print("5. Claude 3 Haiku (экономичная)")

choice = input("\nВаш выбор (1-5, Enter=3): ").strip()

model_map = {
    "1": "gpt-4o",
    "2": "gpt-3.5-turbo",
    "3": "claude-sonnet-4-20250514",
    "4": "claude-3-5-sonnet-20241022",
    "5": "claude-3-haiku-20240307",
    "": "claude-sonnet-4-20250514"
}

selected_model = model_map.get(choice, "claude-sonnet-4-20250514")

# Создаем бота с выбранной моделью
bot = ChatBot()
bot.set_model(selected_model)

print(f"\n✓ Выбрана модель: {bot.get_current_model()}")
print(f"  Режим: {bot.get_mode()}")

# Выбор режима работы
print("\n" + "=" * 70)
print("Выберите режим:")
print("1. Обычный чат")
print("2. Анализ текстового файла")
print("3. Анализ изображения (только для моделей с vision)")

mode_choice = input("\nВаш выбор (1-3, Enter=1): ").strip()

if mode_choice == "2":
    # Анализ текстового файла
    print("\n📝 АНАЛИЗ ТЕКСТОВОГО ФАЙЛА")
    print("-" * 70)
    file_path = input("Введите путь к файлу: ").strip()
    
    if os.path.exists(file_path):
        question = input("Ваш вопрос о файле (Enter для общего анализа): ").strip()
        if not question:
            question = "Проанализируй этот файл и опиши его содержимое"
        
        print("\n⏳ Анализирую файл...")
        try:
            response = bot.chat(question, file_path=file_path)
            
            if isinstance(response, dict):
                # Thinking mode
                print("\n" + "=" * 70)
                if response.get('thinking'):
                    print("🧠 ПРОЦЕСС РАЗМЫШЛЕНИЯ:")
                    print("-" * 70)
                    print(response['thinking'])
                    print("-" * 70)
                print("\n💬 ОТВЕТ:")
                print(response['response'])
                print("=" * 70)
            else:
                # Normal mode
                print("\n💬 ОТВЕТ:")
                print(response)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    else:
        print(f"❌ Файл не найден: {file_path}")

elif mode_choice == "3":
    # Анализ изображения
    print("\n🖼️  АНАЛИЗ ИЗОБРАЖЕНИЯ")
    print("-" * 70)
    
    # Проверяем поддержку vision
    vision_models = get_vision_models()
    current_model = bot.get_current_model()
    
    if current_model not in vision_models:
        print(f"⚠️  Модель {current_model} не поддерживает анализ изображений")
        print("\nМодели с поддержкой vision:")
        for model_id, info in vision_models.items():
            print(f"  - {info.name} ({model_id})")
        
        switch = input("\nПереключиться на gpt-4o? (y/n): ").strip().lower()
        if switch == 'y':
            bot.set_model("gpt-4o")
        else:
            print("Возврат в обычный режим...")
            mode_choice = "1"
    
    if mode_choice == "3":
        file_path = input("Введите путь к изображению: ").strip()
        
        if os.path.exists(file_path):
            question = input("Ваш вопрос об изображении (Enter для общего анализа): ").strip()
            if not question:
                question = "Опиши что изображено на этой картинке"
            
            print("\n⏳ Анализирую изображение...")
            try:
                response = bot.chat(question, file_path=file_path)
                print("\n💬 ОТВЕТ:")
                print(response)
            except Exception as e:
                print(f"❌ Ошибка: {e}")
        else:
            print(f"❌ Файл не найден: {file_path}")

if mode_choice == "1" or mode_choice not in ["2", "3"]:
    # Обычный чат
    print("\n💬 ОБЫЧНЫЙ ЧАТ")
    print("-" * 70)
    print("Команды:")
    print("  'выход' - завершить")
    print("  'модель' - сменить модель")
    print("  'файл' - загрузить файл")
    print("  'модели' - показать все модели")
    print()
    
    while True:
        user_input = input("Вы: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['выход', 'exit', 'quit']:
            print("До свидания!")
            break
        
        if user_input.lower() in ['модель', 'model']:
            print("\nДоступные модели:")
            print("1. gpt-4o")
            print("2. gpt-3.5-turbo")
            print("3. claude-sonnet-4-20250514")
            print("4. claude-3-5-sonnet-20241022")
            model_choice = input("Выберите (1-4): ").strip()
            model_map = {"1": "gpt-4o", "2": "gpt-3.5-turbo", 
                        "3": "claude-sonnet-4-20250514", "4": "claude-3-5-sonnet-20241022"}
            if model_choice in model_map:
                bot.set_model(model_map[model_choice])
            continue
        
        if user_input.lower() in ['файл', 'file']:
            file_path = input("Путь к файлу: ").strip()
            question = input("Вопрос о файле: ").strip()
            try:
                response = bot.chat(question, file_path=file_path)
                if isinstance(response, dict):
                    print(f"\nБот: {response['response']}\n")
                else:
                    print(f"\nБот: {response}\n")
            except Exception as e:
                print(f"Ошибка: {e}\n")
            continue
        
        if user_input.lower() in ['модели', 'models']:
            bot.list_available_models()
            continue
        
        try:
            response = bot.chat(user_input)
            
            if isinstance(response, dict):
                # Thinking mode
                if response.get('thinking'):
                    print(f"\n🧠 Размышление: {response['thinking'][:100]}...")
                print(f"Бот: {response['response']}\n")
            else:
                # Normal mode
                print(f"Бот: {response}\n")
        except Exception as e:
            print(f"Ошибка: {e}\n")

print("\n" + "=" * 70)
print("Демонстрация завершена!")
print("=" * 70)
