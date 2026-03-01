# Структура проекта

## 📁 Файлы проекта

### 🔧 Основные модули
- **chat_bot.py** - Класс ChatBot с полным функционалом
  - Подключение к ProxyAPI.ru
  - Автоматическое сохранение/загрузка истории
  - Управление контекстом диалога
  
- **test_chat.py** - Функциональный подход к работе с API
  - Функции для генерации ответов
  - Интерактивный режим чата
  - Сохранение истории в test_chat_history.json

### 🧪 Тестовые файлы
- **quick_test.py** - Быстрая проверка работоспособности (3 теста)
- **test_persistence.py** - Полный тест сохранения контекста между запусками
- **test_save_load.py** - Простой тест сохранения/загрузки истории
- **demo_persistence.py** - Интерактивная демонстрация (запустите несколько раз!)

### ⚙️ Конфигурация
- **.env** - Переменные окружения (содержит PROXYAPI_KEY)
- **.env.example** - Шаблон для .env файла
- **requirements.txt** - Зависимости проекта
- **.gitignore** - Исключения для git (история, .env, venv)

### 📚 Документация
- **README.md** - Основная документация с инструкциями
- **FEATURES.md** - Подробное описание возможностей
- **PROJECT_STRUCTURE.md** - Этот файл

### 📦 Автоматически создаваемые файлы
- **chat_history.json** - История для chat_bot.py
- **test_chat_history.json** - История для test_chat.py
- **demo_history.json** - История для demo_persistence.py
- **__pycache__/** - Кэш Python
- **.venv/** - Виртуальное окружение

## 🚀 Быстрый старт

1. **Установка**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Настройка**
   - Скопируйте `.env.example` в `.env`
   - Добавьте ваш API ключ от ProxyAPI

3. **Тестирование**
   ```bash
   python quick_test.py           # Быстрая проверка
   python test_persistence.py     # Тест сохранения контекста
   ```

4. **Использование**
   ```bash
   python chat_bot.py             # Интерактивный чат
   python demo_persistence.py     # Демонстрация сохранения
   ```

## 📊 Зависимости

```
openai>=1.0.0          # SDK для работы с OpenAI API
python-dotenv>=1.0.0   # Загрузка переменных окружения
```

## 🔑 Ключевые возможности

✅ Работа через ProxyAPI.ru  
✅ Автоматическое сохранение контекста  
✅ Загрузка истории при запуске  
✅ Поддержка системных промптов  
✅ Команда сброса истории  
✅ Обработка ошибок кодировки  
✅ Интерактивный режим  
✅ Программный API  

## 📝 Примеры использования

### Пример 1: Класс ChatBot
```python
from chat_bot import ChatBot

bot = ChatBot()
bot.set_system_prompt("Ты помощник.")
response = bot.chat("Привет!")
```

### Пример 2: Функциональный подход
```python
from test_chat import generate_response, load_history

load_history()
response = generate_response("Привет!")
```

### Пример 3: Демонстрация сохранения
```bash
# Первый запуск
python demo_persistence.py
> Меня зовут Иван
> выход

# Второй запуск
python demo_persistence.py
> Как меня зовут?
# Ответ: Тебя зовут Иван
```

## 🎯 Рекомендации

1. Используйте `chat_bot.py` для объектно-ориентированного подхода
2. Используйте `test_chat.py` для функционального подхода
3. Запустите `demo_persistence.py` для наглядной демонстрации
4. Проверьте работу с помощью `test_persistence.py`
5. Не коммитьте `.env` и файлы истории в git
