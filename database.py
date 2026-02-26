import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class Database:
    def __init__(self, db_path: str = "wallet_bot.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create trips table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                from_currency TEXT NOT NULL,
                to_currency TEXT NOT NULL,
                rate REAL NOT NULL,
                balance_from REAL NOT NULL,
                balance_to REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

        # Create expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                category TEXT,
                note TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rate_at_time REAL,
                FOREIGN KEY (trip_id) REFERENCES trips (trip_id)
            )
        """)

        # Create budgets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER,
                category TEXT NOT NULL,
                limit_amount REAL NOT NULL,
                spent_amount REAL DEFAULT 0,
                FOREIGN KEY (trip_id) REFERENCES trips (trip_id)
            )
        """)

        conn.commit()
        conn.close()

    def add_user(self, user_id: int, username: str = None):
        """Add a new user to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )

        conn.commit()
        conn.close()

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        conn.close()

        if user:
            return {
                "user_id": user[0],
                "username": user[1],
                "created_at": user[2]
            }
        return None

    def create_trip(self, user_id: int, name: str, from_currency: str, to_currency: str, 
                    rate: float, initial_amount_from: float, initial_amount_to: float) -> int:
        """Create a new trip for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO trips 
            (user_id, name, from_currency, to_currency, rate, balance_from, balance_to) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, name, from_currency, to_currency, rate, initial_amount_from, initial_amount_to))

        trip_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return trip_id

    def get_active_trip(self, user_id: int) -> Optional[Dict]:
        """Get the active trip for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM trips 
            WHERE user_id = ? AND is_active = 1
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))
        trip = cursor.fetchone()

        conn.close()

        if trip:
            return {
                "trip_id": trip[0],
                "user_id": trip[1],
                "name": trip[2],
                "from_currency": trip[3],
                "to_currency": trip[4],
                "rate": trip[5],
                "balance_from": trip[6],
                "balance_to": trip[7],
                "created_at": trip[8],
                "is_active": trip[9]
            }
        return None

    def get_all_trips(self, user_id: int) -> List[Dict]:
        """Get all trips for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM trips WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        trips = cursor.fetchall()

        conn.close()

        return [
            {
                "trip_id": trip[0],
                "user_id": trip[1],
                "name": trip[2],
                "from_currency": trip[3],
                "to_currency": trip[4],
                "rate": trip[5],
                "balance_from": trip[6],
                "balance_to": trip[7],
                "created_at": trip[8],
                "is_active": trip[9]
            } for trip in trips
        ]

    def update_trip_balance(self, trip_id: int, new_balance_from: float, new_balance_to: float):
        """Update the balance of a trip"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE trips 
            SET balance_from = ?, balance_to = ?
            WHERE trip_id = ?
        """, (new_balance_from, new_balance_to, trip_id))

        conn.commit()
        conn.close()

    def add_expense(self, trip_id: int, amount: float, currency: str, category: str = None, 
                    note: str = None, rate_at_time: float = None):
        """Add a new expense to a trip"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses 
            (trip_id, amount, currency, category, note, rate_at_time) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (trip_id, amount, currency, category, note, rate_at_time))

        conn.commit()
        conn.close()

    def get_expenses(self, trip_id: int, limit: int = None) -> List[Dict]:
        """Get all expenses for a trip"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM expenses WHERE trip_id = ? ORDER BY timestamp DESC"
        params = [trip_id]

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        expenses = cursor.fetchall()

        conn.close()

        return [
            {
                "expense_id": exp[0],
                "trip_id": exp[1],
                "amount": exp[2],
                "currency": exp[3],
                "category": exp[4],
                "note": exp[5],
                "timestamp": exp[6],
                "rate_at_time": exp[7]
            } for exp in expenses
        ]

    def get_expenses_by_category(self, trip_id: int) -> Dict[str, float]:
        """Get total expenses grouped by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount) as total 
            FROM expenses 
            WHERE trip_id = ? 
            GROUP BY category
        """, (trip_id,))
        results = cursor.fetchall()

        conn.close()

        return {row[0]: row[1] for row in results if row[0]}

    def set_budget(self, trip_id: int, category: str, limit_amount: float):
        """Set a budget limit for a category in a trip"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO budgets 
            (trip_id, category, limit_amount, spent_amount) 
            VALUES (?, ?, ?, COALESCE((SELECT spent_amount FROM budgets WHERE trip_id = ? AND category = ?), 0))
        """, (trip_id, category, limit_amount, trip_id, category))

        conn.commit()
        conn.close()

    def get_budgets(self, trip_id: int) -> List[Dict]:
        """Get all budgets for a trip"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, limit_amount, spent_amount 
            FROM budgets 
            WHERE trip_id = ?
        """, (trip_id,))
        budgets = cursor.fetchall()

        conn.close()

        return [
            {
                "category": budget[0],
                "limit_amount": budget[1],
                "spent_amount": budget[2]
            } for budget in budgets
        ]

    def update_budget_spent(self, trip_id: int, category: str, new_spent: float):
        """Update the spent amount for a budget category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE budgets 
            SET spent_amount = ? 
            WHERE trip_id = ? AND category = ?
        """, (new_spent, trip_id, category))

        conn.commit()
        conn.close()

    def switch_active_trip(self, user_id: int, trip_id: int):
        """Switch the active trip for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # First deactivate all trips for this user
        cursor.execute("UPDATE trips SET is_active = 0 WHERE user_id = ?", (user_id,))

        # Then activate the selected trip
        cursor.execute("UPDATE trips SET is_active = 1 WHERE trip_id = ?", (trip_id,))

        conn.commit()
        conn.close()

    def update_trip_rate(self, trip_id: int, new_rate: float):
        """Update the exchange rate for a trip"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE trips 
            SET rate = ? 
            WHERE trip_id = ?
        """, (new_rate, trip_id))

        conn.commit()
        conn.close()


# Initialize the database
db = Database()