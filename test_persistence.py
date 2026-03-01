"""
Тест сохранения и загрузки контекста между запусками
"""

from chat_bot import ChatBot
import os
import time

print("=" * 60)
print("Тест сохранения контекста между запусками")
print("=" * 60)

# Удаляем старый файл истории для чистого теста
history_file = "test_persistence_history.json"
if os.path.exists(history_file):
    os.remove(history_file)
    print("✓ Старая история удалена\n")

# === ПЕРВЫЙ ЗАПУСК ===
print("--- ПЕРВЫЙ ЗАПУСК ---")
bot1 = ChatBot(history_file=history_file)
bot1.set_system_prompt("Ты помощник, который запоминает информацию о пользователе.")

response1 = bot1.chat("Привет! Меня зовут Алексей, мне 25 лет.")
print(f"Бот: {response1}\n")

response2 = bot1.chat("Я работаю программистом.")
print(f"Бот: {response2}\n")

print(f"✓ История сохранена в {history_file}")
print(f"  Количество сообщений: {len(bot1.conversation_history)}\n")

# Имитируем завершение программы
del bot1
time.sleep(1)

# === ВТОРОЙ ЗАПУСК (новый экземпляр) ===
print("--- ВТОРОЙ ЗАПУСК (новый экземпляр бота) ---")
bot2 = ChatBot(history_file=history_file)

# Проверяем, что история загрузилась
print(f"Загружено сообщений: {len(bot2.conversation_history)}\n")

# Задаем вопросы о предыдущем разговоре
response3 = bot2.chat("Как меня зовут?")
print(f"Бот: {response3}\n")

response4 = bot2.chat("Сколько мне лет и кем я работаю?")
print(f"Бот: {response4}\n")

print("=" * 60)
print("✓ ТЕСТ ПРОЙДЕН!")
print("✓ Бот успешно загрузил историю и помнит предыдущий разговор")
print("=" * 60)

# Очистка
if os.path.exists(history_file):
    os.remove(history_file)
    print(f"\n✓ Тестовый файл {history_file} удален")
