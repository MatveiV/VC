import os
import json
import logging
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Union, Dict, Any
import time

# Импорт функции работы с думающей моделью Claude
try:
    from testagent import chat_with_thinking_model
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

# Импорт конфигурации моделей и обработчика файлов
try:
    from models_config import get_model_info, ModelInfo, ALL_MODELS
    from file_handler import load_file, format_file_for_prompt, create_vision_message, FileInfo
    MODELS_CONFIG_AVAILABLE = True
except ImportError:
    MODELS_CONFIG_AVAILABLE = False
    print("⚠️  models_config.py или file_handler.py не найдены")

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(
        self, 
        api_key=None, 
        model="gpt-3.5-turbo", 
        history_file="chat_history.json",
        mode="thinking",
        claude_model="claude-sonnet-4-20250514",
        thinking_budget=1500,
        timeout=60,
        max_retries=3
    ):
        """
        Инициализация чат-бота с поддержкой контекста диалога через ProxyAPI.ru
        Поддерживает OpenAI и Claude Extended Thinking через единый ProxyAPI
        
        Args:
            api_key: API ключ от ProxyAPI (если None, берется из переменной окружения PROXYAPI_KEY)
            model: Модель OpenAI или ID любой модели из models_config
            history_file: Путь к файлу для сохранения истории диалога
            mode: Режим работы ("thinking" для Claude, "normal" для OpenAI)
            claude_model: Модель Claude для думающего режима
            thinking_budget: Бюджет токенов для размышлений Claude (default=1500)
            timeout: Таймаут запросов в секундах (default=60)
            max_retries: Максимальное количество повторных попыток (default=3)
        """
        logger.info("=" * 70)
        logger.info("Инициализация ChatBot через ProxyAPI.ru")
        logger.info("=" * 70)
        
        # ProxyAPI конфигурация (единый ключ для всех сервисов)
        api_key = api_key or os.getenv("PROXYAPI_KEY")
        
        if not api_key:
            logger.error("API ключ не найден")
            raise ValueError("API ключ не найден. Укажите api_key или установите переменную окружения PROXYAPI_KEY")
        
        logger.info("✓ API ключ загружен из конфигурации")
        
        # Подключение к ProxyAPI.ru для OpenAI
        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.proxyapi.ru/openai/v1",
                timeout=timeout
            )
            logger.info("✓ OpenAI клиент инициализирован")
        except Exception as e:
            logger.error(f"Ошибка инициализации OpenAI клиента: {e}")
            raise
        
        self.model = model
        self.history_file = history_file
        self.conversation_history = []
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Claude конфигурация (через тот же ProxyAPI ключ)
        self.mode = mode
        self.claude_model = claude_model
        self.thinking_budget = thinking_budget
        
        logger.info(f"✓ Режим работы: {mode}")
        if mode == "thinking":
            logger.info(f"✓ Claude модель: {claude_model}")
            logger.info(f"✓ Бюджет размышлений: {thinking_budget} токенов")
        else:
            logger.info(f"✓ OpenAI модель: {model}")
        
        # Информация о текущей модели
        self.current_model_info = None
        if MODELS_CONFIG_AVAILABLE:
            self.current_model_info = get_model_info(model)
            if self.current_model_info:
                logger.info(f"✓ Информация о модели загружена: {self.current_model_info.name}")
        
        # Автоматически загружаем историю при инициализации
        self.load_history()
        logger.info("=" * 70)
    
    def add_message(self, role, content):
        """Добавить сообщение в историю диалога"""
        self.conversation_history.append({"role": role, "content": content})
    
    def chat(self, user_message, auto_save=True, file_path: Optional[str] = None):
        """
        Отправить сообщение и получить ответ с сохранением контекста
        Поддерживает два режима: thinking (Claude) и normal (OpenAI)
        Поддерживает загрузку файлов для анализа
        
        Args:
            user_message: Сообщение пользователя
            auto_save: Автоматически сохранять историю после каждого сообщения
            file_path: Путь к файлу для анализа (опционально)
            
        Returns:
            str или dict: Ответ ассистента (str для normal, dict для thinking с полной информацией)
        """
        logger.info(f"Получен запрос пользователя (режим: {self.mode})")
        
        # Обработка файла если указан
        file_info = None
        if file_path and MODELS_CONFIG_AVAILABLE:
            try:
                file_info = load_file(file_path)
                logger.info(f"✓ Файл загружен: {file_info.name}")
                print(f"✓ Файл загружен: {file_info.name}")
            except Exception as e:
                logger.error(f"Ошибка загрузки файла: {e}")
                print(f"⚠️  Ошибка загрузки файла: {e}")
                return f"Ошибка загрузки файла: {e}"
        
        # РЕЖИМ THINKING: Claude Extended Thinking
        if self.mode == "thinking" and CLAUDE_AVAILABLE:
            for attempt in range(self.max_retries):
                try:
                    logger.info(f"Попытка {attempt + 1}/{self.max_retries} - Claude Extended Thinking")
                    
                    # Конвертируем историю для Claude
                    claude_history = []
                    system_for_claude = None
                    
                    for msg in self.conversation_history:
                        if msg["role"] == "system":
                            system_for_claude = msg["content"]
                        else:
                            claude_history.append(msg)
                    
                    # Подготовка сообщения с файлом
                    if file_info:
                        if file_info.content:
                            user_message = format_file_for_prompt(file_info, user_message)
                        else:
                            logger.warning("Claude не поддерживает изображения через ProxyAPI")
                            print("⚠️  Claude пока не поддерживает изображения через ProxyAPI")
                            return "Для анализа изображений используйте модели OpenAI с vision (gpt-4o, gpt-4-turbo)"
                    
                    # Вызываем думающую модель через ProxyAPI
                    result = chat_with_thinking_model(
                        user_message=user_message,
                        conversation_history=claude_history,
                        model=self.claude_model,
                        thinking_budget=self.thinking_budget,
                        system_prompt=system_for_claude,
                        api_key=self.api_key,
                        timeout=self.timeout
                    )
                    
                    logger.info("✓ Ответ получен от Claude")
                    logger.info(f"Использовано токенов: {result['usage']['total_tokens']}")
                    
                    # Добавляем в историю
                    self.add_message("user", user_message)
                    self.add_message("assistant", result['response'])
                    
                    # Автоматически сохраняем историю
                    if auto_save:
                        self.save_history()
                    
                    return result
                    
                except Exception as e:
                    logger.error(f"Ошибка в режиме thinking (попытка {attempt + 1}): {e}")
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt  # Экспоненциальная задержка
                        logger.info(f"Повтор через {wait_time} секунд...")
                        time.sleep(wait_time)
                    else:
                        logger.warning("Все попытки исчерпаны, переключаюсь на обычный режим")
                        print(f"⚠️  Ошибка в режиме thinking: {e}")
                        print("Переключаюсь на обычный режим...")
                        self.mode = "normal"
        
        # РЕЖИМ NORMAL: OpenAI через ProxyAPI
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Попытка {attempt + 1}/{self.max_retries} - OpenAI Chat Completions")
                
                # Подготовка сообщения
                message_content = user_message
                
                # Обработка файла для OpenAI
                if file_info:
                    if file_info.content:
                        # Текстовый файл
                        message_content = format_file_for_prompt(file_info, user_message)
                    elif file_info.base64_content:
                        # Изображение - проверяем поддержку vision
                        if self.current_model_info and self.current_model_info.supports_vision:
                            # Используем vision API
                            vision_content = create_vision_message(file_info, user_message)
                            self.add_message("user", vision_content)
                            
                            response = self.client.chat.completions.create(
                                model=self.model,
                                messages=self.conversation_history,
                                timeout=self.timeout
                            )
                            
                            assistant_message = response.choices[0].message.content
                            self.add_message("assistant", assistant_message)
                            
                            logger.info("✓ Ответ получен от OpenAI (vision)")
                            
                            if auto_save:
                                self.save_history()
                            
                            return assistant_message
                        else:
                            logger.warning(f"Модель {self.model} не поддерживает vision")
                            return f"Модель {self.model} не поддерживает анализ изображений. Используйте gpt-4o или gpt-4-turbo."
                
                # Добавляем сообщение пользователя в историю
                self.add_message("user", message_content)
                
                # Отправляем запрос с полной историей диалога
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    timeout=self.timeout
                )
                
                # Получаем ответ ассистента
                assistant_message = response.choices[0].message.content
                
                # Добавляем ответ в историю
                self.add_message("assistant", assistant_message)
                
                logger.info("✓ Ответ получен от OpenAI")
                logger.info(f"Использовано токенов: {response.usage.total_tokens if response.usage else 'N/A'}")
                
                # Автоматически сохраняем историю
                if auto_save:
                    self.save_history()
                
                return assistant_message
                
            except Exception as e:
                logger.error(f"Ошибка в режиме normal (попытка {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Повтор через {wait_time} секунд...")
                    time.sleep(wait_time)
                else:
                    logger.error("Все попытки исчерпаны")
                    raise Exception(f"Не удалось получить ответ после {self.max_retries} попыток: {e}")
    
    def reset_conversation(self):
        """Очистить историю диалога"""
        self.conversation_history = []
        # Удаляем файл истории
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
    
    def set_system_prompt(self, system_message):
        """Установить системный промпт (инструкции для ассистента)"""
        self.conversation_history.insert(0, {"role": "system", "content": system_message})
    
    def set_model(self, model_id: str):
        """Установить модель для использования"""
        if MODELS_CONFIG_AVAILABLE:
            model_info = get_model_info(model_id)
            if model_info:
                if model_info.provider == "claude":
                    self.claude_model = model_id
                    self.mode = "thinking" if model_info.supports_thinking else "normal"
                else:
                    self.model = model_id
                    self.mode = "normal"
                self.current_model_info = model_info
                print(f"✓ Модель изменена на: {model_info.name}")
            else:
                print(f"⚠️  Модель {model_id} не найдена")
        else:
            self.model = model_id
    
    def get_current_model(self) -> str:
        """Получить текущую модель"""
        if self.mode == "thinking":
            return self.claude_model
        return self.model
    
    def list_available_models(self):
        """Вывести список доступных моделей"""
        if MODELS_CONFIG_AVAILABLE:
            from models_config import print_models_table
            print_models_table()
        else:
            print("⚠️  models_config.py не найден")
    
    def set_mode(self, mode):
        """Установить режим работы (thinking или normal)"""
        if mode not in ["thinking", "normal"]:
            raise ValueError("Режим должен быть 'thinking' или 'normal'")
        self.mode = mode
    
    def get_mode(self):
        """Получить текущий режим работы"""
        return self.mode
    
    def save_history(self):
        """Сохранить историю диалога в файл"""
        try:
            data = {
                "model": self.model,
                "mode": self.mode,
                "last_updated": datetime.now().isoformat(),
                "messages": self.conversation_history
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"История сохранена в {self.history_file}")
        except UnicodeEncodeError:
            # Если возникла ошибка кодировки, сохраняем с ensure_ascii=True
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=True, indent=2)
            logger.debug(f"История сохранена в {self.history_file} (ASCII)")
        except Exception as e:
            logger.error(f"Ошибка при сохранении истории: {e}")
            print(f"Ошибка при сохранении истории: {e}")
    
    def load_history(self):
        """Загрузить историю диалога из файла"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation_history = data.get("messages", [])
                    logger.info(f"✓ Загружена история из {self.history_file} ({len(self.conversation_history)} сообщений)")
                    print(f"✓ Загружена история из {self.history_file} ({len(self.conversation_history)} сообщений)")
                    if data.get("last_updated"):
                        logger.info(f"  Последнее обновление: {data['last_updated']}")
                        print(f"  Последнее обновление: {data['last_updated']}")
            else:
                logger.info("История не найдена, начинаем новый диалог")
        except Exception as e:
            logger.error(f"Ошибка при загрузке истории: {e}")
            print(f"Ошибка при загрузке истории: {e}")
            self.conversation_history = []


# Пример использования
if __name__ == "__main__":
    # Выбор режима работы
    print("=" * 70)
    print("Чат-бот через ProxyAPI.ru (OpenAI + Claude Extended Thinking)")
    print("=" * 70)
    print("\n🤖 ВЫБОР РЕЖИМА РАБОТЫ:")
    print("1. Thinking Mode (Claude Extended Thinking) - думающая модель [По умолчанию]")
    print("2. Normal Mode (OpenAI) - обычная модель")
    
    choice = input("\nВыберите режим (1/2, Enter=1): ").strip()
    
    if choice == "2":
        mode = "normal"
        print("\n✓ Выбран режим: Normal Mode (OpenAI)")
    else:
        mode = "thinking"
        print("\n✓ Выбран режим: Thinking Mode (Claude)")
        if CLAUDE_AVAILABLE:
            print("  Бюджет токенов для размышлений: 1500")
            print("  Подключение через: ProxyAPI.ru")
    
    # Создаем экземпляр чат-бота
    bot = ChatBot(mode=mode)
    
    # Опционально: устанавливаем системный промпт
    bot.set_system_prompt("Ты дружелюбный помощник, который отвечает кратко и по делу.")
    
    print("\nЧат-бот запущен через ProxyAPI.ru!")
    print("Команды: 'выход' - завершить, 'сброс' - очистить историю, 'режим' - сменить режим")
    print("История автоматически сохраняется в chat_history.json\n")
    
    # Простой цикл диалога
    while True:
        user_input = input("Вы: ")
        
        if user_input.lower() in ['выход', 'exit', 'quit']:
            print("До свидания!")
            break
        
        if user_input.lower() in ['сброс', 'reset']:
            bot.reset_conversation()
            print("✓ История диалога очищена\n")
            continue
        
        if user_input.lower() in ['режим', 'mode']:
            print("\n🔄 Смена режима:")
            print("1. Thinking Mode (Claude)")
            print("2. Normal Mode (OpenAI)")
            mode_choice = input("Выберите (1/2): ").strip()
            
            if mode_choice == "2":
                bot.set_mode("normal")
                print(f"✓ Переключено на Normal Mode\n")
            else:
                bot.set_mode("thinking")
                print(f"✓ Переключено на Thinking Mode\n")
            continue
        
        if not user_input.strip():
            continue
        
        try:
            response = bot.chat(user_input)
            
            # Форматируем вывод в зависимости от режима
            if bot.get_mode() == "thinking" and isinstance(response, dict):
                # Красивый вывод для думающей модели
                print("\n" + "=" * 70)
                if response.get('thinking'):
                    print("🧠 ПРОЦЕСС РАЗМЫШЛЕНИЯ:")
                    print("-" * 70)
                    print(response['thinking'])
                    print("-" * 70)
                print("\n💬 ОТВЕТ:")
                print(response['response'])
                print("=" * 70 + "\n")
            else:
                # Обычный вывод
                response_text = response if isinstance(response, str) else response.get('response', str(response))
                print(f"Бот: {response_text}\n")
                
        except Exception as e:
            print(f"Ошибка: {e}\n")
