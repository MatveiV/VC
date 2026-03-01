"""
Демонстрация работы сохранения контекста
Запустите этот файл несколько раз подряд, чтобы увидеть, как бот помнит предыдущие разговоры
"""

from chat_bot import ChatBot

print("=" * 60)
print("Демонстрация сохранения контекста")
print("=" * 60)
print()

# Создаем бота (история загружается автоматически)
bot = ChatBot(history_file="demo_history.json")

# Если история пустая, устанавливаем системный промпт
if len(bot.conversation_history) == 0:
    bot.set_system_prompt("Ты дружелюбный помощник, который запоминает информацию о пользователе.")
    print("Новый диалог начат!")
else:
    print(f"Продолжаем предыдущий диалог ({len(bot.conversation_history)} сообщений в истории)")

print()
print("Команды:")
print("  - Введите сообщение для общения с ботом")
print("  - 'сброс' - очистить историю и начать заново")
print("  - 'выход' - завершить программу")
print()
print("История автоматически сохраняется после каждого сообщения.")
print("Запустите программу снова, чтобы продолжить разговор!")
print()

while True:
    user_input = input("Вы: ").strip()
    
    if not user_input:
        continue
    
    if user_input.lower() in ['выход', 'exit', 'quit']:
        print("\nДо свидания! Ваша история сохранена в demo_history.json")
        print("Запустите программу снова, чтобы продолжить разговор.")
        break
    
    if user_input.lower() in ['сброс', 'reset']:
        bot.reset_conversation()
        bot.set_system_prompt("Ты дружелюбный помощник, который запоминает информацию о пользователе.")
        print("✓ История очищена. Начинаем новый диалог!\n")
        continue
    
    try:
        response = bot.chat(user_input)
        print(f"Бот: {response}\n")
    except Exception as e:
        print(f"Ошибка: {e}\n")
