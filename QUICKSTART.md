# 🚀 Быстрый старт

## Установка за 3 шага

### 1️⃣ Создайте виртуальное окружение
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 2️⃣ Установите зависимости
```bash
pip install -r requirements.txt
```

### 3️⃣ Настройте API ключ
Создайте файл `.env`:
```
PROXYAPI_KEY=ваш_ключ_от_proxyapi
```

Получить ключ: https://proxyapi.ru

## ✅ Проверка работоспособности

```bash
python quick_test.py
```

Вы должны увидеть:
```
✓ Все тесты пройдены успешно!
✓ Бот запоминает контекст диалога
✓ Подключение к ProxyAPI.ru работает
```

## 🎮 Попробуйте демо

### Демонстрация сохранения контекста
```bash
python demo_persistence.py
```

Введите:
```
Меня зовут Иван
выход
```

Запустите снова:
```bash
python demo_persistence.py
```

Введите:
```
Как меня зовут?
```

Бот ответит: "Тебя зовут Иван" ✨

## 💻 Использование в коде

### Вариант 1: Класс ChatBot
```python
from chat_bot import ChatBot

bot = ChatBot()
bot.set_system_prompt("Ты помощник программиста.")
response = bot.chat("Объясни async/await")
print(response)
```

### Вариант 2: Функции
```python
from test_chat import generate_response

response = generate_response("Привет!")
print(response)
```

## 📝 Интерактивный режим

```bash
python chat_bot.py
```

Команды:
- Просто пишите сообщения для общения
- `сброс` - очистить историю
- `выход` - завершить

## 🧪 Тесты

```bash
# Быстрая проверка
python quick_test.py

# Тест сохранения контекста
python test_persistence.py

# Простой тест
python test_save_load.py
```

## 📚 Дополнительная информация

- [README.md](README.md) - Полная документация
- [FEATURES.md](FEATURES.md) - Описание возможностей
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Структура проекта

## ❓ Частые вопросы

**Q: Где хранится история диалога?**  
A: В JSON файлах: `chat_history.json`, `test_chat_history.json`, `demo_history.json`

**Q: Как очистить историю?**  
A: Используйте команду `сброс` в интерактивном режиме или `bot.reset_conversation()` в коде

**Q: Можно ли использовать другие модели?**  
A: Да! Укажите при создании: `ChatBot(model="gpt-4")`

**Q: История сохраняется автоматически?**  
A: Да, после каждого сообщения

## 🎯 Готово!

Теперь вы можете:
- ✅ Общаться с ботом через ProxyAPI.ru
- ✅ Сохранять и загружать историю диалогов
- ✅ Использовать в своих проектах
- ✅ Настраивать поведение через системные промпты
