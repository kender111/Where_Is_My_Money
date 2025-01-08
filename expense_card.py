import tkinter as tk
from tkinter import ttk

class ExpenseCard(tk.Toplevel):
    def __init__(self, parent, data_manager, day, month, year, update_expenses_callback):
        super().__init__(parent)
        self.data_manager = data_manager
        self.day = day
        self.month = month
        self.year = year
        self.update_expenses_callback = update_expenses_callback
        self.selected_expense = None

        self.title("Деталі витрат")
        self.geometry("600x400")
        
        # Створюємо таблицю для витрат
        self.expenses_treeview = ttk.Treeview(self, columns=("name", "amount", "category", "expense_type"), show="headings")
        self.expenses_treeview.heading("name", text="Назва")
        self.expenses_treeview.heading("amount", text="Сума")
        self.expenses_treeview.heading("category", text="Категорія")
        self.expenses_treeview.heading("expense_type", text="Тип")
        
        self.expenses_treeview.pack(fill="both", expand=True, pady=10)

        # Кнопки для редагування та видалення
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="Додати витрату", command=self.add_expense)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(button_frame, text="Редагувати", state=tk.DISABLED, command=self.edit_expense)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(button_frame, text="Видалити", state=tk.DISABLED, command=self.delete_expense)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Оновлюємо відображення витрат
        self.display_expenses()

    def display_expenses(self):
        # Очищаємо таблицю перед оновленням
        for item in self.expenses_treeview.get_children():
            self.expenses_treeview.delete(item)

        # Отримуємо витрати за даний день
        expenses = self.data_manager.get_expenses_for_day(self.day, self.month, self.year)
        
        # Додаємо кожну витрату в таблицю
        for expense in expenses:
            self.expenses_treeview.insert("", "end", values=(expense['name'], expense['amount'], expense['category'], expense['expense_type']))

        # Додаємо функціональність для вибору витрати
        self.expenses_treeview.bind("<ButtonRelease-1>", self.select_expense)

    def select_expense(self, event):
        # Отримуємо вибрану витрату
        selected_item = self.expenses_treeview.selection()
        if selected_item:
            selected_expense_data = self.expenses_treeview.item(selected_item)["values"]
            self.selected_expense = {
                "name": selected_expense_data[0],
                "amount": selected_expense_data[1],
                "category": selected_expense_data[2],
                "expense_type": selected_expense_data[3]
            }
            # Оновлюємо відображення деталей вибраної витрати
            self.show_selected_expense_details(self.selected_expense)

            # Активуємо кнопки редагування та видалення
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)

    def show_selected_expense_details(self, expense):
        # Оновлюємо відображення інформації про витрату
        details_text = f"Назва: {expense['name']}\n" \
                       f"Сума: {expense['amount']} грн\n" \
                       f"Категорія: {expense['category']}\n" \
                       f"Тип: {expense['expense_type']}"
        
        # Якщо є елемент для відображення деталей (наприклад, Label)
        if hasattr(self, 'expense_details_label'):
            self.expense_details_label.config(text=details_text)
        else:
            # Створюємо нову мітку для відображення деталей, якщо її немає
            self.expense_details_label = tk.Label(self, text=details_text, font=("Helvetica", 10))
            self.expense_details_label.pack(pady=10)

    def edit_expense(self):
        # Логіка для редагування витрати
        if self.selected_expense:
            print(f"Редагувати витрату: {self.selected_expense['name']}")
            # Тому тут ви можете реалізувати відкриття форми для редагування витрати

    def delete_expense(self):
        # Логіка для видалення витрати
        if self.selected_expense:
            print(f"Видалити витрату: {self.selected_expense['name']}")
            self.data_manager.delete_expense(self.selected_expense['name'], self.day, self.month, self.year)
            self.update_expenses_callback()  # Оновлюємо список витрат після видалення
            self.display_expenses()  # Оновлюємо відображення таблиці витрат

    def add_expense(self):
        # Логіка для додавання витрати
        print("Додавання нової витрати...")
        # Можна відкрити нове вікно для введення витрати або додати інший механізм додавання
