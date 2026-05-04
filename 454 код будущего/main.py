import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "workouts.json"

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - План тренировок")
        self.root.geometry("800x600")

        # Загрузка данных
        self.workouts = self.load_data()

        # --- Интерфейс ввода ---
        input_frame = ttk.LabelFrame(root, text="Новая тренировка", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        # Подсказка по формату
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky="w")
        self.type_entry = ttk.Entry(input_frame)
        self.type_entry.grid(row=0, column=3, padx=5, pady=5)

        # Длительность (минуты)
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, sticky="w")
        self.duration_entry = ttk.Entry(input_frame)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)

        # Кнопка добавления
        add_btn = ttk.Button(input_frame, text="Добавить", command=self.add_workout)
        add_btn.grid(row=0, column=6, padx=10)

        # --- Интерфейс фильтрации ---
        filter_frame = ttk.LabelFrame(root, text="Фильтр", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, sticky="w")
        self.filter_type = ttk.Entry(filter_frame)
        self.filter_type.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=2, sticky="w")
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=3, padx=5)

        filter_btn = ttk.Button(filter_frame, text="Применить", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=5)

        reset_btn = ttk.Button(filter_frame, text="Сброс", command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5)

        # --- Таблица ---
        tree_frame = ttk.Frame(root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Дата", "Тип", "Длительность (мин)")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Кнопка удаления
        del_btn = ttk.Button(root, text="Удалить выбранное", command=self.delete_workout)
        del_btn.pack(pady=5)

        self.refresh_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.workouts, f, ensure_ascii=False, indent=4)

    def validate_input(self, date_str, w_type, duration_str):
        # Проверка пустых полей
        if not date_str or not w_type or not duration_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return False

        # Проверка формата даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД.")
            return False

        # Проверка длительности
        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным целым числом.")
            return False

        return True

    def add_workout(self):
        date_str = self.date_entry.get().strip()
        w_type = self.type_entry.get().strip()
        duration_str = self.duration_entry.get().strip()

        if not self.validate_input(date_str, w_type, duration_str):
            return

        new_workout = {
            "id": len(self.workouts) + 1,
            "date": date_str,
            "type": w_type,
            "duration": int(duration_str)
        }

        self.workouts.append(new_workout)
        self.save_data()
        self.refresh_table()

        # Очистка полей (кроме даты, удобно оставлять текущую)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Тренировка добавлена в план!")

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_data = data if data is not None else self.workouts
        
        for w in display_
            self.tree.insert("", tk.END, values=(
                w["id"],
                w["date"],
                w["type"],
                w["duration"]
            ))

    def apply_filter(self):
        type_filter = self.filter_type.get().strip().lower()
        date_filter = self.filter_date.get().strip()

        filtered_data = self.workouts

        if type_filter:
            filtered_data = [w for w in filtered_data if type_filter in w["type"].lower()]
        
        if date_filter:
            filtered_data = [w for w in filtered_data if w["date"] == date_filter]

        self.refresh_table(filtered_data)

    def reset_filter(self):
        self.filter_type.delete(0, tk.END)
        self.filter_date.delete(0, tk.END)
        self.refresh_table()

    def delete_workout(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите запись для удаления!")
            return
        
        item_values = self.tree.item(selected_item[0])["values"]
        workout_id = item_values[0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить тренировку ID {workout_id}?"):
            self.workouts = [w for w in self.workouts if w["id"] != workout_id]
            self.save_data()
            self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
    