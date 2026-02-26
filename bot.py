import telebot
from telebot import types
import re
from datetime import datetime
from api_client import convert_currency, get_current_rate
from database import db
from config import TELEGRAM_BOT_TOKEN
import matplotlib.pyplot as plt
import io


# Initialize bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Dictionary to store user states
user_states = {}

# Expense categories
CATEGORIES = ['Транспорт', 'Жильё', 'Еда', 'Развлечения', 'Сувениры', 'Другое']

# Regular expression to check if message is a number
NUMBER_PATTERN = re.compile(r'^\d+(\.\d+)?$')


def format_currency(amount, currency):
    """Format currency amount with proper formatting"""
    return f"{amount:.2f} {currency}"


def get_main_menu():
    """Create main menu inline keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_new_trip = types.InlineKeyboardButton("✈️ Создать новое путешествие", callback_data="new_trip")
    btn_my_trips = types.InlineKeyboardButton("🧳 Мои путешествия", callback_data="my_trips")
    btn_balance = types.InlineKeyboardButton("💰 Баланс", callback_data="balance")
    btn_history = types.InlineKeyboardButton("📊 История расходов", callback_data="history")
    btn_set_rate = types.InlineKeyboardButton("🔄 Изменить курс", callback_data="set_rate")
    
    markup.add(btn_new_trip, btn_my_trips, btn_balance, btn_history, btn_set_rate)
    return markup


def get_category_buttons():
    """Create inline keyboard with expense categories"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    for category in CATEGORIES:
        button = types.InlineKeyboardButton(category, callback_data=f"cat_{category}")
        buttons.append(button)
    
    markup.add(*buttons)
    return markup


def check_budget_limit(user_id, trip_id, category, expense_amount):
    """Check if expense exceeds budget limit for category"""
    budgets = db.get_budgets(trip_id)
    for budget in budgets:
        if budget['category'] == category:
            new_spent = budget['spent_amount'] + expense_amount
            if new_spent >= budget['limit_amount'] * 0.9:  # Warning at 90% of limit
                remaining = budget['limit_amount'] - new_spent
                percent_left = (remaining / budget['limit_amount']) * 100
                
                warning_msg = f"⚠️ Внимание! Осталось менее 10% бюджета на '{category}'!\n"
                if percent_left > 0:
                    warning_msg += f"Осталось: {format_currency(remaining, 'RUB')} ({percent_left:.1f}%)"
                else:
                    warning_msg += f"Бюджет превышен на {format_currency(abs(remaining), 'RUB')}!"
                
                return warning_msg
    return None


def generate_expense_chart(trip_id):
    """Generate pie chart of expenses by category"""
    expenses_by_category = db.get_expenses_by_category(trip_id)
    
    if not expenses_by_category:
        return None
    
    categories = list(expenses_by_category.keys())
    amounts = list(expenses_by_category.values())
    
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Расходы по категориям')
    
    # Save plot to bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Add user to database
    db.add_user(user_id, username)
    
    welcome_text = (
        "👋 Привет! Я ваш персональный мини-кошелёк для путешествий.\n\n"
        "Я помогу вам управлять расходами в разных валютах во время поездок.\n\n"
        "Выберите действие:"
    )
    
    bot.reply_to(message, welcome_text, reply_markup=get_main_menu())


@bot.message_handler(commands=['newtrip'])
def create_new_trip_command(message):
    """Handle /newtrip command"""
    bot.reply_to(message, "Введите название путешествия:")
    user_states[message.chat.id] = {'state': 'waiting_trip_name'}


@bot.message_handler(commands=['switch'])
def switch_trip_command(message):
    """Handle /switch command"""
    user_id = message.from_user.id
    trips = db.get_all_trips(user_id)
    
    if not trips:
        bot.reply_to(message, "У вас пока нет путешествий.")
        return
    
    markup = types.InlineKeyboardMarkup()
    for trip in trips:
        btn = types.InlineKeyboardButton(
            f"{trip['name']} ({trip['to_currency']})",
            callback_data=f"switch_trip_{trip['trip_id']}"
        )
        markup.add(btn)
    
    bot.reply_to(message, "Выберите путешествие:", reply_markup=markup)


@bot.message_handler(commands=['balance'])
def show_balance_command(message):
    """Handle /balance command"""
    user_id = message.from_user.id
    trip = db.get_active_trip(user_id)
    
    if not trip:
        bot.reply_to(message, "У вас нет активного путешествия. Создайте его сначала.")
        return
    
    balance_text = (
        f"💳 Баланс в активном путешествии '{trip['name']}':\n\n"
        f"Основная валюта: {format_currency(trip['balance_from'], trip['from_currency'])}\n"
        f"Целевая валюта: {format_currency(trip['balance_to'], trip['to_currency'])}\n\n"
        f"Текущий курс: 1 {trip['from_currency']} = {trip['rate']} {trip['to_currency']}"
    )
    
    bot.reply_to(message, balance_text)


@bot.message_handler(commands=['history'])
def show_history_command(message):
    """Handle /history command"""
    user_id = message.from_user.id
    trip = db.get_active_trip(user_id)
    
    if not trip:
        bot.reply_to(message, "У вас нет активного путешествия. Создайте его сначала.")
        return
    
    expenses = db.get_expenses(trip['trip_id'], limit=10)  # Last 10 expenses
    
    if not expenses:
        bot.reply_to(message, "История расходов пуста.")
        return
    
    history_text = f"📜 Последние расходы в '{trip['name']}':\n\n"
    for expense in expenses:
        history_text += (
            f"• {format_currency(expense['amount'], expense['currency'])} "
            f"({expense['category'] or 'Без категории'}) - {expense['timestamp'][:19]}\n"
        )
    
    # Add chart option
    markup = types.InlineKeyboardMarkup()
    btn_chart = types.InlineKeyboardButton("📈 Показать график расходов", callback_data="show_chart")
    markup.add(btn_chart)
    
    bot.reply_to(message, history_text, reply_markup=markup)


@bot.message_handler(commands=['setrate'])
def set_rate_command(message):
    """Handle /setrate command"""
    user_id = message.from_user.id
    trip = db.get_active_trip(user_id)
    
    if not trip:
        bot.reply_to(message, "У вас нет активного путешествия. Создайте его сначала.")
        return
    
    bot.reply_to(message, f"Введите новый курс для {trip['from_currency']} → {trip['to_currency']}:")
    user_states[message.chat.id] = {'state': 'waiting_new_rate', 'trip_id': trip['trip_id']}


@bot.message_handler(func=lambda message: NUMBER_PATTERN.match(message.text) and user_states.get(message.chat.id, {}).get('state') is None)
def handle_expense(message):
    """Handle expense input (numbers only)"""
    user_id = message.from_user.id
    trip = db.get_active_trip(user_id)
    
    if not trip:
        bot.reply_to(message, "У вас нет активного путешествия. Сначала создайте его.")
        return
    
    try:
        amount = float(message.text)
        
        # Calculate converted amount
        converted_amount = amount / trip['rate'] if trip['rate'] != 0 else 0
        
        # Format the message
        expense_text = (
            f"💸 Подтвердите расход:\n\n"
            f"{format_currency(amount, trip['to_currency'])} = "
            f"{format_currency(converted_amount, trip['from_currency'])}\n\n"
            f"Баланс до: {format_currency(trip['balance_to'], trip['to_currency'])} → "
            f"После: {format_currency(trip['balance_to'] - amount, trip['to_currency'])}"
        )
        
        # Create inline buttons for confirmation
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_yes = types.InlineKeyboardButton("✅ Да", callback_data=f"confirm_expense_{amount}")
        btn_no = types.InlineKeyboardButton("❌ Нет", callback_data="cancel_expense")
        markup.add(btn_yes, btn_no)
        
        bot.reply_to(message, expense_text, reply_markup=markup)
        
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректное число.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_trip_name')
def process_trip_name(message):
    """Process trip name input"""
    user_id = message.from_user.id
    trip_name = message.text
    
    user_states[message.chat.id] = {
        'state': 'waiting_from_currency',
        'trip_name': trip_name
    }
    
    bot.reply_to(message, "Введите код исходной валюты (например, RUB):")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_from_currency')
def process_from_currency(message):
    """Process source currency input"""
    from_currency = message.text.upper()
    
    user_states[message.chat.id]['from_currency'] = from_currency
    user_states[message.chat.id]['state'] = 'waiting_to_currency'
    
    bot.reply_to(message, "Введите код целевой валюты (например, USD):")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_to_currency')
def process_to_currency(message):
    """Process target currency input"""
    user_id = message.from_user.id
    to_currency = message.text.upper()
    
    state_data = user_states[message.chat.id]
    from_currency = state_data['from_currency']
    trip_name = state_data['trip_name']
    
    # Get current rate from API
    rate_data = convert_currency(1, from_currency, to_currency)
    
    if not rate_data.get('success'):
        error_info = rate_data.get('error', {}).get('info', 'Неизвестная ошибка')
        bot.reply_to(message, f"Ошибка получения курса: {error_info}. Попробуйте еще раз.")
        return
    
    rate = rate_data.get('result', 1)  # Default to 1 if no result found
    
    # Store the rate temporarily and ask for initial amount
    state_data['to_currency'] = to_currency
    state_data['rate'] = rate
    state_data['state'] = 'waiting_initial_amount'
    
    bot.reply_to(
        message, 
        f"Текущий курс: 1 {from_currency} = {rate} {to_currency}\n\n"
        f"Введите начальную сумму в {from_currency}:"
    )


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_initial_amount')
def process_initial_amount(message):
    """Process initial amount input"""
    try:
        initial_amount_from = float(message.text)
        
        state_data = user_states[message.chat.id]
        from_currency = state_data['from_currency']
        to_currency = state_data['to_currency']
        rate = state_data['rate']
        trip_name = state_data['trip_name']
        
        # Calculate initial amount in target currency
        initial_amount_to = initial_amount_from * rate
        
        # Create trip in database
        trip_id = db.create_trip(
            user_id=message.from_user.id,
            name=trip_name,
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate,
            initial_amount_from=initial_amount_from,
            initial_amount_to=initial_amount_to
        )
        
        # Clear user state
        del user_states[message.chat.id]
        
        bot.reply_to(
            message,
            f"✅ Путешествие '{trip_name}' создано!\n\n"
            f"Исходная валюта: {format_currency(initial_amount_from, from_currency)}\n"
            f"Целевая валюта: {format_currency(initial_amount_to, to_currency)}\n"
            f"Курс: 1 {from_currency} = {rate} {to_currency}"
        )
        
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректное число.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_new_rate')
def process_new_rate(message):
    """Process new rate input"""
    try:
        new_rate = float(message.text)
        
        state_data = user_states[message.chat.id]
        trip_id = state_data['trip_id']
        
        # Update rate in database
        db.update_trip_rate(trip_id, new_rate)
        
        # Clear user state
        del user_states[message.chat.id]
        
        bot.reply_to(message, f"✅ Курс успешно обновлен: 1 → {new_rate}")
        
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректное число.")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Handle all callback queries"""
    user_id = call.from_user.id
    
    if call.data == "new_trip":
        bot.send_message(call.message.chat.id, "Введите название путешествия:")
        user_states[call.message.chat.id] = {'state': 'waiting_trip_name'}
        
    elif call.data == "my_trips":
        trips = db.get_all_trips(user_id)
        
        if not trips:
            bot.send_message(call.message.chat.id, "У вас пока нет путешествий.")
        else:
            markup = types.InlineKeyboardMarkup()
            for trip in trips:
                btn = types.InlineKeyboardButton(
                    f"{trip['name']} ({trip['to_currency']})",
                    callback_data=f"switch_trip_{trip['trip_id']}"
                )
                markup.add(btn)
            
            bot.send_message(call.message.chat.id, "Ваши путешествия:", reply_markup=markup)
            
    elif call.data == "balance":
        trip = db.get_active_trip(user_id)
        
        if not trip:
            bot.send_message(call.message.chat.id, "У вас нет активного путешествия. Создайте его сначала.")
        else:
            balance_text = (
                f"💳 Баланс в активном путешествии '{trip['name']}':\n\n"
                f"Основная валюта: {format_currency(trip['balance_from'], trip['from_currency'])}\n"
                f"Целевая валюта: {format_currency(trip['balance_to'], trip['to_currency'])}\n\n"
                f"Текущий курс: 1 {trip['from_currency']} = {trip['rate']} {trip['to_currency']}"
            )
            
            bot.send_message(call.message.chat.id, balance_text)
            
    elif call.data == "history":
        trip = db.get_active_trip(user_id)
        
        if not trip:
            bot.send_message(call.message.chat.id, "У вас нет активного путешествия. Создайте его сначала.")
        else:
            expenses = db.get_expenses(trip['trip_id'], limit=10)  # Last 10 expenses
            
            if not expenses:
                bot.send_message(call.message.chat.id, "История расходов пуста.")
            else:
                history_text = f"📜 Последние расходы в '{trip['name']}':\n\n"
                for expense in expenses:
                    history_text += (
                        f"• {format_currency(expense['amount'], expense['currency'])} "
                        f"({expense['category'] or 'Без категории'}) - {expense['timestamp'][:19]}\n"
                    )
                
                # Add chart option
                markup = types.InlineKeyboardMarkup()
                btn_chart = types.InlineKeyboardButton("📈 Показать график расходов", callback_data="show_chart")
                markup.add(btn_chart)
                
                bot.send_message(call.message.chat.id, history_text, reply_markup=markup)
                
    elif call.data == "set_rate":
        trip = db.get_active_trip(user_id)
        
        if not trip:
            bot.send_message(call.message.chat.id, "У вас нет активного путешествия. Создайте его сначала.")
        else:
            bot.send_message(
                call.message.chat.id, 
                f"Введите новый курс для {trip['from_currency']} → {trip['to_currency']}:"
            )
            user_states[call.message.chat.id] = {'state': 'waiting_new_rate', 'trip_id': trip['trip_id']}
            
    elif call.data.startswith("switch_trip_"):
        trip_id = int(call.data.split("_")[2])
        
        # Switch active trip
        db.switch_active_trip(user_id, trip_id)
        
        # Get updated trip info
        trip = db.get_active_trip(user_id)
        
        bot.send_message(
            call.message.chat.id,
            f"✅ Активное путешествие изменено на '{trip['name']}'\n"
            f"Валюта: {trip['to_currency']}"
        )
        
    elif call.data.startswith("confirm_expense_"):
        amount = float(call.data.split("_")[2])
        
        # Get active trip
        trip = db.get_active_trip(user_id)
        
        if not trip:
            bot.send_message(call.message.chat.id, "У вас нет активного путешествия.")
            return
        
        # Calculate converted amount
        converted_amount = amount / trip['rate'] if trip['rate'] != 0 else 0
        
        # Check if we have enough balance
        if trip['balance_to'] < amount:
            bot.send_message(call.message.chat.id, "❌ Недостаточно средств для этого расхода!")
            return
        
        # Update balances
        new_balance_from = trip['balance_from'] - converted_amount
        new_balance_to = trip['balance_to'] - amount
        
        # Update trip balance in database
        db.update_trip_balance(trip['trip_id'], new_balance_from, new_balance_to)
        
        # Ask for category
        bot.send_message(
            call.message.chat.id,
            f"✅ Расход {format_currency(amount, trip['to_currency'])} подтвержден!\n\n"
            f"Выберите категорию расхода:",
            reply_markup=get_category_buttons()
        )
        
        # Store expense info for category selection
        user_states[call.message.chat.id] = {
            'state': 'waiting_category',
            'expense_data': {
                'trip_id': trip['trip_id'],
                'amount': amount,
                'currency': trip['to_currency'],
                'rate_at_time': trip['rate']
            }
        }
        
    elif call.data == "cancel_expense":
        bot.send_message(call.message.chat.id, "❌ Расход отменен.")
        
    elif call.data.startswith("cat_"):
        category = call.data[4:]  # Remove "cat_" prefix
        
        if user_states.get(call.message.chat.id, {}).get('state') == 'waiting_category':
            expense_data = user_states[call.message.chat.id]['expense_data']
            
            # Add expense to database
            db.add_expense(
                trip_id=expense_data['trip_id'],
                amount=expense_data['amount'],
                currency=expense_data['currency'],
                category=category,
                rate_at_time=expense_data['rate_at_time']
            )
            
            # Update budget spent amount if budget exists
            db.update_budget_spent(
                expense_data['trip_id'],
                category,
                db.get_budgets(expense_data['trip_id'])[0].get('spent_amount', 0) + expense_data['amount']
            )
            
            # Check budget limit
            budget_warning = check_budget_limit(
                user_id, 
                expense_data['trip_id'], 
                category, 
                expense_data['amount']
            )
            
            if budget_warning:
                bot.send_message(call.message.chat.id, budget_warning)
            
            # Clear user state
            del user_states[call.message.chat.id]
            
            bot.send_message(
                call.message.chat.id,
                f"✅ Расход в категории '{category}' успешно добавлен!"
            )
    
    elif call.data == "show_chart":
        trip = db.get_active_trip(user_id)
        
        if not trip:
            bot.send_message(call.message.chat.id, "У вас нет активного путешествия.")
            return
        
        chart_buffer = generate_expense_chart(trip['trip_id'])
        
        if chart_buffer:
            bot.send_photo(call.message.chat.id, chart_buffer)
        else:
            bot.send_message(call.message.chat.id, "Недостаточно данных для построения графика.")
    
    # Answer callback query
    bot.answer_callback_query(call.id)


if __name__ == '__main__':
    print("Bot is starting...")
    bot.polling(none_stop=True)