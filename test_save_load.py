"""
Простой тест сохранения и загрузки истории
"""

from chat_bot import ChatBot
import os

print("Тест 1: Создание нового диалога")
print("-" * 50)

# Удаляем старую историю
if os.path.exists("test_save_history.json"):
    os.remove("test_save_history.json")

# Создаем бота и начинаем диалог
bot = ChatBot(history_file="test_save_history.json")
bot.set_system_prompt("Ты помощник.")

response1 = bot.chat("Привет! Меня зовут Мария.")
print(f"Ответ 1: {response1[:100]}...")

print(f"\n✓ Сохранено сообщений: {len(bot.conversation_history)}")
print(f"✓ Файл создан: {os.path.exists('test_save_history.json')}")

# Удаляем бота
del bot

print("\nТест 2: Загрузка истории в новом экземпляре")
print("-" * 50)

# Создаем новый экземпляр
bot2 = ChatBot(history_file="test_save_history.json")

print(f"✓ Загружено сообщений: {len(bot2.conversation_history)}")

# Проверяем память
response2 = bot2.chat("Как меня зовут?")
print(f"Ответ 2: {response2}")

print("\n✓ Тест завершен успешно!")

# Очистка
os.remove("test_save_history.json")
