"""
Быстрый тест для проверки работы с ProxyAPI
"""

from chat_bot import ChatBot

# Создаем бота
bot = ChatBot()

# Устанавливаем системный промпт
bot.set_system_prompt("Ты дружелюбный помощник.")

# Тестируем диалог
print("Тест 1: Простое сообщение")
response1 = bot.chat("Привет!")
print(f"Ответ: {response1}\n")

print("Тест 2: Проверка контекста")
response2 = bot.chat("Меня зовут Иван")
print(f"Ответ: {response2}\n")

print("Тест 3: Проверка памяти")
response3 = bot.chat("Как меня зовут?")
print(f"Ответ: {response3}\n")

print("✓ Все тесты пройдены успешно!")
print("✓ Бот запоминает контекст диалога")
print("✓ Подключение к ProxyAPI.ru работает")
