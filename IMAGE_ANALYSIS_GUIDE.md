# 🖼️ Руководство по анализу изображений PNG

## Как это работает

Проект использует **Vision API** от OpenAI для анализа изображений. Изображения конвертируются в формат base64 и отправляются вместе с текстовым запросом.

### Поддерживаемые форматы изображений:
- `.png` ✅
- `.jpg` / `.jpeg` ✅
- `.gif` ✅
- `.webp` ✅
- `.bmp` ✅

### Модели с поддержкой Vision:
- **gpt-4o** (рекомендуется) ✅
- **gpt-4-turbo** ✅
- **claude-3-5-sonnet-20241022** ✅
- **claude-3-opus-20240229** ✅
- **claude-3-sonnet-20240229** ✅

---

## 📝 Способы прикрепления изображений

### 1. Через параметр `file_path` (рекомендуется)

```python
from chat_bot import ChatBot

# Создаем бота с моделью, поддерживающей vision
bot = ChatBot(model="gpt-4o", mode="normal")

# Анализируем изображение
response = bot.chat(
    "Что изображено на этой картинке?",
    file_path="photo.png"
)

print(response)
```

### 2. Через интерактивный режим

```bash
python chat_bot.py
```

В чате введите команду `файл`:
```
Вы: файл
Путь к файлу: photo.png
Вопрос о файле: Опиши что на картинке
```

### 3. Через демонстрационный скрипт

```bash
python demo_models_and_files.py
```

Выберите:
- Модель с vision (например, gpt-4o)
- Режим "3. Анализ изображения"
- Укажите путь к PNG файлу

---

## 💻 Примеры использования

### Пример 1: Простой анализ изображения

```python
from chat_bot import ChatBot

bot = ChatBot(model="gpt-4o", mode="normal")

# Общий анализ
response = bot.chat(
    "Опиши это изображение детально",
    file_path="screenshot.png"
)
print(response)
```

### Пример 2: Извлечение текста с изображения (OCR)

```python
from chat_bot import ChatBot

bot = ChatBot(model="gpt-4o", mode="normal")

response = bot.chat(
    "Извлеки весь текст с этого изображения",
    file_path="document.png"
)
print(response)
```

### Пример 3: Анализ диаграммы или графика

```python
from chat_bot import ChatBot

bot = ChatBot(model="gpt-4o", mode="normal")

response = bot.chat(
    "Проанализируй этот график и объясни основные тренды",
    file_path="chart.png"
)
print(response)
```

### Пример 4: Анализ кода на скриншоте

```python
from chat_bot import ChatBot

bot = ChatBot(model="gpt-4o", mode="normal")

response = bot.chat(
    "Объясни что делает этот код и найди возможные ошибки",
    file_path="code_screenshot.png"
)
print(response)
```

### Пример 5: Сравнение изображений (последовательно)

```python
from chat_bot import ChatBot

bot = ChatBot(model="gpt-4o", mode="normal")

# Первое изображение
response1 = bot.chat(
    "Запомни это изображение",
    file_path="image1.png"
)

# Второе изображение
response2 = bot.chat(
    "Сравни это изображение с предыдущим. Какие отличия?",
    file_path="image2.png"
)
print(response2)
```

---

## 🔧 Техническая реализация

### Шаг 1: Загрузка изображения

```python
from file_handler import load_file

# Загружаем PNG файл
file_info = load_file("photo.png")

# file_info содержит:
# - name: "photo.png"
# - size: размер в байтах
# - mime_type: "image/png"
# - base64_content: base64 строка изображения
```

### Шаг 2: Создание Vision сообщения

```python
from file_handler import create_vision_message

# Создаем структуру для Vision API
content = create_vision_message(
    file_info,
    user_question="Что на картинке?"
)

# content = [
#     {
#         "type": "text",
#         "text": "Что на картинке?"
#     },
#     {
#         "type": "image_url",
#         "image_url": {
#             "url": "data:image/png;base64,iVBORw0KGgo..."
#         }
#     }
# ]
```

### Шаг 3: Отправка в OpenAI Vision API

```python
from openai import OpenAI

client = OpenAI(
    api_key="your_key",
    base_url="https://api.proxyapi.ru/openai/v1"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": content  # Структура с текстом и изображением
        }
    ]
)

print(response.choices[0].message.content)
```

---

## 📁 Работа с путями к файлам

### Абсолютный путь

```python
bot.chat(
    "Анализируй",
    file_path="C:/Users/User/Pictures/photo.png"
)
```

### Относительный путь (от текущей директории)

```python
bot.chat(
    "Анализируй",
    file_path="images/photo.png"
)
```

### Путь в той же папке

```python
bot.chat(
    "Анализируй",
    file_path="photo.png"
)
```

---

## ⚠️ Важные замечания

### 1. Модель должна поддерживать Vision

```python
# ✅ Правильно - модель с vision
bot = ChatBot(model="gpt-4o")
response = bot.chat("Анализируй", file_path="photo.png")

# ❌ Неправильно - модель без vision
bot = ChatBot(model="gpt-3.5-turbo")
response = bot.chat("Анализируй", file_path="photo.png")
# Ошибка: "Модель gpt-3.5-turbo не поддерживает анализ изображений"
```

### 2. Проверка поддержки Vision

```python
from models_config import get_vision_models

# Получить все модели с vision
vision_models = get_vision_models()

for model_id, info in vision_models.items():
    print(f"{info.name} - {model_id}")

# Вывод:
# GPT-4o - gpt-4o
# GPT-4 Turbo - gpt-4-turbo
# Claude 3.5 Sonnet - claude-3-5-sonnet-20241022
# ...
```

### 3. Размер файла

- Рекомендуемый размер: до 20 MB
- Изображение автоматически конвертируется в base64
- Большие изображения могут увеличить время обработки

### 4. Claude и изображения

⚠️ **Важно:** Claude через ProxyAPI пока не поддерживает изображения в текущей реализации.

```python
# ❌ Не работает
bot = ChatBot(mode="thinking")  # Claude
response = bot.chat("Анализируй", file_path="photo.png")
# Вернет: "Для анализа изображений используйте модели OpenAI с vision"

# ✅ Используйте OpenAI
bot = ChatBot(mode="normal", model="gpt-4o")
response = bot.chat("Анализируй", file_path="photo.png")
```

---

## 🎯 Практические сценарии

### Сценарий 1: Анализ UI/UX дизайна

```python
bot = ChatBot(model="gpt-4o", mode="normal")

response = bot.chat(
    """
    Проанализируй этот дизайн интерфейса:
    1. Оцени удобство использования
    2. Укажи на проблемы с доступностью
    3. Предложи улучшения
    """,
    file_path="ui_design.png"
)
```

### Сценарий 2: Проверка документов

```python
bot = ChatBot(model="gpt-4o", mode="normal")

response = bot.chat(
    "Извлеки все данные из этого документа и структурируй в JSON",
    file_path="invoice.png"
)
```

### Сценарий 3: Анализ медицинских изображений (общий)

```python
bot = ChatBot(model="gpt-4o", mode="normal")

response = bot.chat(
    "Опиши что видно на этом медицинском снимке (только описание, не диагноз)",
    file_path="xray.png"
)
```

### Сценарий 4: Распознавание объектов

```python
bot = ChatBot(model="gpt-4o", mode="normal")

response = bot.chat(
    "Перечисли все объекты на этом изображении с их количеством",
    file_path="scene.png"
)
```

---

## 🧪 Тестирование

### Создайте тестовое изображение

```python
# test_image_analysis.py
from chat_bot import ChatBot
import os

# Проверяем наличие тестового изображения
if not os.path.exists("test_image.png"):
    print("⚠️  Создайте файл test_image.png для тестирования")
    exit(1)

# Создаем бота
bot = ChatBot(model="gpt-4o", mode="normal")

# Тест 1: Общий анализ
print("Тест 1: Общий анализ")
response = bot.chat(
    "Опиши это изображение",
    file_path="test_image.png"
)
print(response)
print()

# Тест 2: Извлечение текста
print("Тест 2: Извлечение текста")
response = bot.chat(
    "Есть ли текст на изображении? Если да, извлеки его",
    file_path="test_image.png"
)
print(response)
```

---

## 📊 Стоимость

Анализ изображений через Vision API:

| Модель | Стоимость (за изображение) |
|--------|---------------------------|
| gpt-4o | ~$0.01 - $0.05 |
| gpt-4-turbo | ~$0.02 - $0.10 |

*Зависит от размера изображения и длины ответа*

---

## 🔗 Дополнительные ресурсы

- [OpenAI Vision API Documentation](https://platform.openai.com/docs/guides/vision)
- [file_handler.py](file_handler.py) - исходный код обработки файлов
- [models_config.py](models_config.py) - список моделей с vision
- [demo_models_and_files.py](demo_models_and_files.py) - интерактивная демонстрация

---

## ❓ FAQ

**Q: Можно ли анализировать несколько изображений одновременно?**  
A: Да, но последовательно. Отправьте первое изображение, затем второе с контекстом предыдущего.

**Q: Поддерживаются ли анимированные GIF?**  
A: Да, но анализируется только первый кадр.

**Q: Можно ли использовать URL изображения вместо файла?**  
A: В текущей версии нет, только локальные файлы. Можно добавить эту функцию.

**Q: Какое максимальное разрешение изображения?**  
A: OpenAI автоматически масштабирует изображения. Рекомендуется до 2048x2048 пикселей.

**Q: Работает ли с прозрачными PNG?**  
A: Да, прозрачность сохраняется при конвертации в base64.

---

**Версия:** 2.3  
**Дата:** 2026-03-01  
**Автор:** Senior Developer
