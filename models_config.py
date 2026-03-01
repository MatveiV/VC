"""
Конфигурация доступных моделей ИИ через ProxyAPI.ru
Поддержка OpenAI и Claude с различными версиями
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ModelInfo:
    """Информация о модели"""
    id: str
    name: str
    provider: str  # "openai" или "claude"
    description: str
    max_tokens: int
    supports_thinking: bool = False
    supports_vision: bool = False
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0


# Доступные модели OpenAI
OPENAI_MODELS = {
    "gpt-4o": ModelInfo(
        id="gpt-4o",
        name="GPT-4o",
        provider="openai",
        description="Самая продвинутая модель OpenAI с поддержкой изображений",
        max_tokens=128000,
        supports_vision=True,
        cost_per_1k_input=2.5,
        cost_per_1k_output=10.0
    ),
    "gpt-4-turbo": ModelInfo(
        id="gpt-4-turbo",
        name="GPT-4 Turbo",
        provider="openai",
        description="Быстрая версия GPT-4 с большим контекстом",
        max_tokens=128000,
        supports_vision=True,
        cost_per_1k_input=10.0,
        cost_per_1k_output=30.0
    ),
    "gpt-4": ModelInfo(
        id="gpt-4",
        name="GPT-4",
        provider="openai",
        description="Мощная модель для сложных задач",
        max_tokens=8192,
        cost_per_1k_input=30.0,
        cost_per_1k_output=60.0
    ),
    "gpt-3.5-turbo": ModelInfo(
        id="gpt-3.5-turbo",
        name="GPT-3.5 Turbo",
        provider="openai",
        description="Быстрая и экономичная модель для большинства задач",
        max_tokens=16385,
        cost_per_1k_input=0.5,
        cost_per_1k_output=1.5
    ),
}

# Доступные модели Claude
CLAUDE_MODELS = {
    "claude-sonnet-4-20250514": ModelInfo(
        id="claude-sonnet-4-20250514",
        name="Claude Sonnet 4 (Extended Thinking)",
        provider="claude",
        description="Думающая модель с процессом размышления",
        max_tokens=200000,
        supports_thinking=True,
        cost_per_1k_input=3.0,
        cost_per_1k_output=15.0
    ),
    "claude-3-5-sonnet-20241022": ModelInfo(
        id="claude-3-5-sonnet-20241022",
        name="Claude 3.5 Sonnet",
        provider="claude",
        description="Быстрая и мощная модель для большинства задач",
        max_tokens=200000,
        supports_vision=True,
        cost_per_1k_input=3.0,
        cost_per_1k_output=15.0
    ),
    "claude-3-opus-20240229": ModelInfo(
        id="claude-3-opus-20240229",
        name="Claude 3 Opus",
        provider="claude",
        description="Самая мощная модель Claude для сложных задач",
        max_tokens=200000,
        supports_vision=True,
        cost_per_1k_input=15.0,
        cost_per_1k_output=75.0
    ),
    "claude-3-sonnet-20240229": ModelInfo(
        id="claude-3-sonnet-20240229",
        name="Claude 3 Sonnet",
        provider="claude",
        description="Баланс между скоростью и качеством",
        max_tokens=200000,
        supports_vision=True,
        cost_per_1k_input=3.0,
        cost_per_1k_output=15.0
    ),
    "claude-3-haiku-20240307": ModelInfo(
        id="claude-3-haiku-20240307",
        name="Claude 3 Haiku",
        provider="claude",
        description="Самая быстрая и экономичная модель Claude",
        max_tokens=200000,
        cost_per_1k_input=0.25,
        cost_per_1k_output=1.25
    ),
}

# Все доступные модели
ALL_MODELS = {**OPENAI_MODELS, **CLAUDE_MODELS}


def get_model_info(model_id: str) -> Optional[ModelInfo]:
    """Получить информацию о модели по ID"""
    return ALL_MODELS.get(model_id)


def list_models(provider: Optional[str] = None) -> Dict[str, ModelInfo]:
    """
    Получить список доступных моделей
    
    Args:
        provider: Фильтр по провайдеру ("openai", "claude" или None для всех)
    
    Returns:
        Словарь моделей
    """
    if provider == "openai":
        return OPENAI_MODELS
    elif provider == "claude":
        return CLAUDE_MODELS
    else:
        return ALL_MODELS


def get_thinking_models() -> Dict[str, ModelInfo]:
    """Получить модели с поддержкой Extended Thinking"""
    return {k: v for k, v in ALL_MODELS.items() if v.supports_thinking}


def get_vision_models() -> Dict[str, ModelInfo]:
    """Получить модели с поддержкой изображений"""
    return {k: v for k, v in ALL_MODELS.items() if v.supports_vision}


def print_models_table():
    """Вывести таблицу доступных моделей"""
    print("\n" + "=" * 100)
    print("ДОСТУПНЫЕ МОДЕЛИ ИИ")
    print("=" * 100)
    
    print("\n📊 OpenAI Models:")
    print("-" * 100)
    for model_id, info in OPENAI_MODELS.items():
        vision = "🖼️ " if info.supports_vision else ""
        print(f"  {vision}{info.name}")
        print(f"    ID: {info.id}")
        print(f"    {info.description}")
        print(f"    Контекст: {info.max_tokens:,} токенов")
        print(f"    Стоимость: ${info.cost_per_1k_input}/1K вход, ${info.cost_per_1k_output}/1K выход")
        print()
    
    print("\n🧠 Claude Models:")
    print("-" * 100)
    for model_id, info in CLAUDE_MODELS.items():
        thinking = "💭 " if info.supports_thinking else ""
        vision = "🖼️ " if info.supports_vision else ""
        print(f"  {thinking}{vision}{info.name}")
        print(f"    ID: {info.id}")
        print(f"    {info.description}")
        print(f"    Контекст: {info.max_tokens:,} токенов")
        print(f"    Стоимость: ${info.cost_per_1k_input}/1K вход, ${info.cost_per_1k_output}/1K выход")
        print()
    
    print("=" * 100)
    print("\nЛегенда:")
    print("  💭 - Поддержка Extended Thinking (процесс размышления)")
    print("  🖼️  - Поддержка анализа изображений")
    print("=" * 100)


if __name__ == "__main__":
    # Демонстрация
    print_models_table()
    
    print("\n\nПримеры использования:")
    print("-" * 50)
    
    # Получить информацию о модели
    model = get_model_info("gpt-4o")
    if model:
        print(f"\nИнформация о {model.name}:")
        print(f"  Провайдер: {model.provider}")
        print(f"  Поддержка изображений: {model.supports_vision}")
        print(f"  Макс. токенов: {model.max_tokens:,}")
    
    # Список думающих моделей
    print("\n\nМодели с Extended Thinking:")
    for model_id, info in get_thinking_models().items():
        print(f"  - {info.name} ({model_id})")
    
    # Список моделей с vision
    print("\n\nМодели с поддержкой изображений:")
    for model_id, info in get_vision_models().items():
        print(f"  - {info.name} ({model_id})")
