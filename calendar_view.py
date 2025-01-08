import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from expense_card import ExpenseCard

class CalendarView(tk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_date = datetime.today()
        self.selected_day = None  # Додано для зберігання вибраного дня
        self.selected_expense = None  # Додано для зберігання вибраної витрати
        self.draw_calendar()

    def draw_calendar(self):
        # Очищаємо попередній вміст вікна
        for widget in self.winfo_children():
            widget.destroy()

        # Відображення планки з місяцем і роком
        header_frame = tk.Frame(self)
        header_frame.pack()

        # Кнопка для попереднього місяця
        prev_month_button = tk.Button(header_frame, text="<", command=self.prev_month)
        prev_month_button.pack(side=tk.LEFT)

        # Мітка з поточним місяцем і роком
        label = tk.Label(header_frame, text=f"{self.current_date.strftime('%B')} {self.current_date.year}", font=("Helvetica", 16))
        label.pack(side=tk.LEFT, padx=10)

        # Кнопка для наступного місяця
        next_month_button = tk.Button(header_frame, text=">", command=self.next_month)
        next_month_button.pack(side=tk.LEFT)

        # Місце для календаря
        calendar_frame = tk.Frame(self)
        calendar_frame.pack()

        # Дні тижня
        days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        for i, day_name in enumerate(days_of_week):
            day_label = tk.Label(calendar_frame, text=day_name, font=("Helvetica", 12), width=4, height=2, relief="solid")
            day_label.grid(row=0, column=i)

        # Дні місяця
        first_day_of_month = datetime(self.current_date.year, self.current_date.month, 1)
        last_day_of_month = self.get_last_day_of_month(self.current_date.month, self.current_date.year)
        start_day = first_day_of_month.weekday()

        # Відображення кнопок для кожного дня
        day = 1
        for row in range(1, 7):  # 6 рядків для днів
            for col in range(7):  # 7 стовпців для днів тижня
                if (row == 1 and col >= start_day) or (row > 1 and day <= last_day_of_month.day):
                    self.create_day_button(calendar_frame, day, row, col)
                    day += 1

    def create_day_button(self, calendar_frame, day, row, col):
        button = tk.Button(calendar_frame, text=str(day), width=10, height=3, bg="#d3d3d3", fg="black", font=("Helvetica", 12))
        button.grid(row=row, column=col, padx=5, pady=5)

        # Отримуємо витрати для дня
        expenses = self.data_manager.get_expenses_for_day(day, self.current_date.month, self.current_date.year)

        # Додати кольорову індикацію витрат
        if expenses:  # Якщо витрати є
            button.config(bg="lightcoral")  # Червоний фон
        else:  # Якщо витрат немає
            button.config(bg="lightgreen")  # Зелений фон

        # Оновлюємо витрати після додавання
        button.bind("<Button-1>", lambda event, day=day: self.open_expenses_window(day))

    def open_expenses_window(self, day):
        # Оновлюємо вибраний день
        self.selected_day = day

        # Отримуємо витрати для вибраного дня
        expenses = self.data_manager.get_expenses_for_day(day, self.current_date.month, self.current_date.year)

        if not expenses:
            messagebox.showinfo("Інформація", "В цьому дні немає витрат.")
            return

        # Відкриваємо вікно витрат і передаємо місяць, рік та функцію оновлення витрат
        ExpenseCard(self, self.data_manager, day, self.current_date.month, self.current_date.year, self.update_expenses)

    def update_expenses(self):
        # Оновлення витрат: перерисовка календаря
        self.draw_calendar()

    def prev_month(self):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.draw_calendar()

    def next_month(self):
        # Перехід до наступного місяця
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.draw_calendar()

    def get_last_day_of_month(self, month, year):
        # Отримуємо останній день місяця
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return last_day
