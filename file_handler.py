"""
Модуль для работы с файлами
Поддержка загрузки, чтения и преобразования различных форматов
"""

import os
import base64
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class FileInfo:
    """Информация о файле"""
    path: str
    name: str
    size: int
    mime_type: str
    extension: str
    content: Optional[str] = None
    base64_content: Optional[str] = None


# Поддерживаемые текстовые форматы
TEXT_FORMATS = {
    '.txt', '.md', '.py', '.js', '.ts', '.jsx', '.tsx',
    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
    '.csv', '.html', '.css', '.scss', '.sass',
    '.java', '.cpp', '.c', '.h', '.hpp',
    '.go', '.rs', '.rb', '.php', '.sh', '.bat',
    '.sql', '.r', '.m', '.swift', '.kt'
}

# Поддерживаемые форматы изображений
IMAGE_FORMATS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'
}

# Поддерживаемые форматы документов
DOCUMENT_FORMATS = {
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
}


def get_file_info(file_path: str) -> FileInfo:
    """
    Получить информацию о файле
    
    Args:
        file_path: Путь к файлу
    
    Returns:
        FileInfo объект с информацией о файле
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    # Определяем MIME тип
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"
    
    return FileInfo(
        path=str(path.absolute()),
        name=path.name,
        size=path.stat().st_size,
        mime_type=mime_type,
        extension=path.suffix.lower()
    )


def read_text_file(file_path: str, encoding: str = 'utf-8') -> str:
    """
    Прочитать текстовый файл
    
    Args:
        file_path: Путь к файлу
        encoding: Кодировка файла
    
    Returns:
        Содержимое файла
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Попробуем другие кодировки
        for enc in ['cp1251', 'latin-1', 'utf-16']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read()
            except:
                continue
        raise ValueError(f"Не удалось прочитать файл с поддерживаемой кодировкой")


def read_image_file(file_path: str) -> str:
    """
    Прочитать изображение и конвертировать в base64
    
    Args:
        file_path: Путь к файлу
    
    Returns:
        Base64 строка
    """
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def load_file(file_path: str) -> FileInfo:
    """
    Загрузить файл и подготовить для отправки в AI
    
    Args:
        file_path: Путь к файлу
    
    Returns:
        FileInfo с загруженным содержимым
    """
    info = get_file_info(file_path)
    
    # Текстовые файлы
    if info.extension in TEXT_FORMATS:
        info.content = read_text_file(file_path)
        print(f"✓ Загружен текстовый файл: {info.name} ({info.size} байт)")
    
    # Изображения
    elif info.extension in IMAGE_FORMATS:
        info.base64_content = read_image_file(file_path)
        print(f"✓ Загружено изображение: {info.name} ({info.size} байт)")
    
    # Документы (пока только информация)
    elif info.extension in DOCUMENT_FORMATS:
        print(f"⚠️  Формат {info.extension} требует дополнительной обработки")
        print(f"   Файл: {info.name} ({info.size} байт)")
        raise NotImplementedError(f"Формат {info.extension} пока не поддерживается напрямую")
    
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {info.extension}")
    
    return info


def format_file_for_prompt(file_info: FileInfo, user_question: str = "") -> str:
    """
    Форматировать файл для отправки в промпт
    
    Args:
        file_info: Информация о файле
        user_question: Вопрос пользователя
    
    Returns:
        Отформатированный промпт
    """
    prompt_parts = []
    
    if user_question:
        prompt_parts.append(user_question)
        prompt_parts.append("")
    
    prompt_parts.append(f"Файл: {file_info.name}")
    prompt_parts.append(f"Размер: {file_info.size} байт")
    prompt_parts.append(f"Тип: {file_info.mime_type}")
    prompt_parts.append("")
    
    if file_info.content:
        prompt_parts.append("Содержимое файла:")
        prompt_parts.append("```")
        prompt_parts.append(file_info.content)
        prompt_parts.append("```")
    
    return "\n".join(prompt_parts)


def create_vision_message(file_info: FileInfo, user_question: str = "") -> List[Dict[str, Any]]:
    """
    Создать сообщение для моделей с поддержкой vision
    
    Args:
        file_info: Информация о файле (изображение)
        user_question: Вопрос пользователя
    
    Returns:
        Список блоков контента для API
    """
    if not file_info.base64_content:
        raise ValueError("Файл должен быть изображением с base64 контентом")
    
    content = []
    
    # Текстовая часть
    if user_question:
        content.append({
            "type": "text",
            "text": user_question
        })
    else:
        content.append({
            "type": "text",
            "text": "Проанализируй это изображение и опиши что на нем изображено."
        })
    
    # Изображение
    content.append({
        "type": "image_url",
        "image_url": {
            "url": f"data:{file_info.mime_type};base64,{file_info.base64_content}"
        }
    })
    
    return content


def get_supported_formats() -> Dict[str, List[str]]:
    """Получить список поддерживаемых форматов"""
    return {
        "text": sorted(list(TEXT_FORMATS)),
        "image": sorted(list(IMAGE_FORMATS)),
        "document": sorted(list(DOCUMENT_FORMATS))
    }


def print_supported_formats():
    """Вывести список поддерживаемых форматов"""
    formats = get_supported_formats()
    
    print("\n" + "=" * 70)
    print("ПОДДЕРЖИВАЕМЫЕ ФОРМАТЫ ФАЙЛОВ")
    print("=" * 70)
    
    print("\n📝 Текстовые файлы (полная поддержка):")
    print("   " + ", ".join(formats["text"]))
    
    print("\n🖼️  Изображения (для моделей с vision):")
    print("   " + ", ".join(formats["image"]))
    
    print("\n📄 Документы (требуют дополнительной обработки):")
    print("   " + ", ".join(formats["document"]))
    
    print("\n" + "=" * 70)


# Тестирование
if __name__ == "__main__":
    print_supported_formats()
    
    print("\n\nПримеры использования:")
    print("-" * 70)
    
    # Пример с текстовым файлом
    print("\n1. Загрузка текстового файла:")
    print("   file_info = load_file('example.py')")
    print("   prompt = format_file_for_prompt(file_info, 'Объясни этот код')")
    
    # Пример с изображением
    print("\n2. Загрузка изображения:")
    print("   file_info = load_file('image.jpg')")
    print("   content = create_vision_message(file_info, 'Что на картинке?')")
    
    print("\n" + "-" * 70)
