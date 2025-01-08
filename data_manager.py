import sqlite3

class DataManager:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)  # Підключення до БД
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    day INTEGER,
                    month INTEGER,
                    year INTEGER,
                    name TEXT,
                    amount REAL,
                    category TEXT,
                    expense_type TEXT
                )
            """)
    
    def get_expenses_for_day(self, day, month, year):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, day, month, year, name, amount, category, expense_type
            FROM expenses 
            WHERE day = ? AND month = ? AND year = ?
        """, (day, month, year))
        
        # Отримуємо всі записи
        rows = cursor.fetchall()

        # Перетворюємо кожен запис в словник
        expenses = []
        for row in rows:
            expense = dict(zip([column[0] for column in cursor.description], row))
            expenses.append(expense)
        
        return expenses

    def add_expense(self, day, month, year, name, amount, category, expense_type):
        with self.connection:
            self.connection.execute("""
                INSERT INTO expenses (day, month, year, name, amount, category, expense_type) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (day, month, year, name, amount, category, expense_type))

    def delete_expense(self, expense_name, day, month, year):
        with self.connection:
            self.connection.execute("""
                DELETE FROM expenses 
                WHERE name = ? AND day = ? AND month = ? AND year = ?
            """, (expense_name, day, month, year))

    def close(self):
        self.connection.close()
