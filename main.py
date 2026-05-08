import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        # Создаем поля ввода
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Дата
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w")
        self.entry_date = tk.Entry(self.root)
        self.entry_date.grid(row=0, column=1)

        # Тип тренировки
        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, sticky="w")
        self.entry_type = tk.Entry(self.root)
        self.entry_type.grid(row=1, column=1)

        # Длительность
        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, sticky="w")
        self.entry_duration = tk.Entry(self.root)
        self.entry_duration.grid(row=2, column=1)

        # Кнопка добавить
        self.btn_add = tk.Button(self.root, text="Добавить тренировку", command=self.add_training)
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self.root, columns=("date", "type", "duration"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность")
        self.tree.grid(row=4, column=0, columnspan=2)

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=5, column=0, sticky="w")
        self.filter_type_var = tk.StringVar()
        self.filter_type_entry = ttk.Combobox(self.root, textvariable=self.filter_type_var)
        self.filter_type_entry['values'] = []  # позже заполняется
        self.filter_type_entry.grid(row=5, column=1)
        self.filter_type_entry.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        tk.Label(self.root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=6, column=0, sticky="w")
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1)
        self.filter_date.bind("<KeyRelease>", lambda e: self.apply_filter())

        # Кнопки для сохранения и загрузки
        self.btn_save = tk.Button(self.root, text="Сохранить в JSON", command=self.save_data)
        self.btn_save.grid(row=7, column=0, pady=10)
        self.btn_load = tk.Button(self.root, text="Загрузить из JSON", command=self.load_data)
        self.btn_load.grid(row=7, column=1, pady=10)

    def add_training(self):
        date_str = self.entry_date.get()
        type_str = self.entry_type.get()
        duration_str = self.entry_duration.get()

        # Валидация даты
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return

        # Валидация типа тренировки
        if not type_str:
            messagebox.showerror("Ошибка", "Поле 'Тип тренировки' не должно быть пустым.")
            return
        
        # Валидация длительности
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        # Добавляю данные
        record = {
            "date": date_str,
            "type": type_str,
            "duration": int(duration_str)
        }
        self.data.append(record)
        self.update_table()
        self.update_filters()

        # Очистка полей
        self.entry_date.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def update_table(self, filtered_data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data_to_show = filtered_data if filtered_data is not None else self.data
        for item in data_to_show:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def update_filters(self):
        types = set(item["type"] for item in self.data)
        self.filter_type_entry['values'] = ["Все"] + sorted(types)
        self.filter_type_var.set("Все")

    def apply_filter(self):
        filtered = self.data
        t_filter = self.filter_type_var.get()
        d_filter = self.filter_date.get()

        if t_filter != "Все" and t_filter != "":
            filtered = [item for item in filtered if item["type"] == t_filter]
        if d_filter != "":
            try:
                datetime.strptime(d_filter, "%Y-%m-%d")
                filtered = [item for item in filtered if item["date"] == d_filter]
            except ValueError:
                pass  # игнорируем некорректный формат

        self.update_table(filtered)

    def save_data(self):
        with open("training_data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранение", "Данные успешно сохранены.")

    def load_data(self):
        if os.path.exists("training_data.json"):
            with open("training_data.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.update_table()
            self.update_filters()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
