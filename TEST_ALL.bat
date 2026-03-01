@echo off
echo ========================================
echo Запуск всех тестов проекта
echo ========================================
echo.

echo [1/3] Быстрая проверка работоспособности...
.venv\Scripts\python.exe quick_test.py
if %errorlevel% neq 0 (
    echo ОШИБКА: quick_test.py завершился с ошибкой
    pause
    exit /b 1
)
echo.

echo [2/3] Тест сохранения контекста между запусками...
.venv\Scripts\python.exe test_persistence.py
if %errorlevel% neq 0 (
    echo ОШИБКА: test_persistence.py завершился с ошибкой
    pause
    exit /b 1
)
echo.

echo [3/3] Простой тест сохранения/загрузки...
.venv\Scripts\python.exe test_save_load.py
if %errorlevel% neq 0 (
    echo ОШИБКА: test_save_load.py завершился с ошибкой
    pause
    exit /b 1
)
echo.

echo ========================================
echo ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
echo ========================================
echo.
echo Проект готов к использованию!
echo.
echo Попробуйте:
echo   - python chat_bot.py
echo   - python demo_persistence.py
echo.
pause
