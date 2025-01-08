from tkinter import Tk
from calendar_view import CalendarView
from data_manager import DataManager

def main():
    data_manager = DataManager()
    root = Tk()
    root.title("Гроші, де ви?")
    calendar_view = CalendarView(root, data_manager)
    calendar_view.pack(expand=True, fill="both")
    root.mainloop()

if __name__ == "__main__":
    main()
