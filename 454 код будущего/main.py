import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# --- Глобальные переменные ---
DATA_FILE = "workouts.json"
workouts_list = []  # Список для хранения тренировок

# Элементы интерфейса (будут инициализированы в create_interface)
tree = None
date_entry = None
type_entry = None
duration_entry = None
filter_type_entry = None
filter_date_entry = None

def load_data():
    """Загрузка данных из JSON файла."""
    global workouts_list
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                workouts_list = json.load(f)
        except json.JSONDecodeError:
            workouts_list = []
    else:
        workouts_list = []

def save_data():
    """Сохранение данных в JSON файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(workouts_list, f, ensure_ascii=False, indent=4)

def get_next_id():
    """Генерация уникального ID."""
    if not workouts_list:
        return 1
    return max(w["id"] for w in workouts_list) + 1

def validate_input(date_str, w_type, duration_str):
    """Проверка введенных данных."""
    if not date_str or not w_type or not duration_str:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return False

    # Проверка даты
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

def add_workout():
    """Добавление новой тренировки."""
    global workouts_list
    
    date_str = date_entry.get().strip()
    w_type = type_entry.get().strip()
    duration_str = duration_entry.get().strip()

    if not validate_input(date_str, w_type, duration_str):
        return

    new_workout = {
        "id": get_next_id(),
        "date": date_str,
        "type": w_type,
        "duration": int(duration_str)
    }

    workouts_list.append(new_workout)
    save_data()
    refresh_table()

    # Очистка полей ввода
    type_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    
    messagebox.showinfo("Успех", "Тренировка добавлена!")

def refresh_table(data=None):
    """Обновление таблицы с данными."""
    global tree
    
    # Очищаем таблицу
    for item in tree.get_children():
        tree.delete(item)
    
    # Выбираем данные для отображения (все или отфильтрованные)
    display_data = data if data is not None else workouts_list
    
    # Заполняем таблицу
    for w in display_data:
        tree.insert("", tk.END, values=(
            w["id"],
            w["date"],
            w["type"],
            w["duration"]
        ))

def apply_filter():
    """Применение фильтрации."""
    type_filter = filter_type_entry.get().strip().lower()
    date_filter = filter_date_entry.get().strip()

    filtered_data = workouts_list

    if type_filter:
        filtered_data = [w for w in filtered_data if type_filter in w["type"].lower()]
    
    if date_filter:
        filtered_data = [w for w in filtered_data if w["date"] == date_filter]

    refresh_table(filtered_data)

def reset_filter():
    """Сброс фильтров."""
    filter_type_entry.delete(0, tk.END)
    filter_date_entry.delete(0, tk.END)
    refresh_table()

def delete_workout():
    """Удаление выбранной тренировки."""
    global workouts_list
    
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Внимание", "Выберите запись для удаления!")
        return
    
    item_values = tree.item(selected_item[0])["values"]
    workout_id = item_values[0]
    
    if messagebox.askyesno("Подтверждение", f"Удалить тренировку ID {workout_id}?"):
        workouts_list = [w for w in workouts_list if w["id"] != workout_id]
        save_data()
        refresh_table()

def create_interface(root):
    """Создание графического интерфейса."""
    global tree, date_entry, type_entry, duration_entry, filter_type_entry, filter_date_entry

    root.title("Training Planner - План тренировок")
    root.geometry("800x600")

    # --- Фрейм ввода ---
    input_frame = ttk.LabelFrame(root, text="Новая тренировка", padding=10)
    input_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w")
    date_entry = ttk.Entry(input_frame)
    date_entry.grid(row=0, column=1, padx=5, pady=5)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky="w")
    type_entry = ttk.Entry(input_frame)
    type_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, sticky="w")
    duration_entry = ttk.Entry(input_frame)
    duration_entry.grid(row=0, column=5, padx=5, pady=5)

    add_btn = ttk.Button(input_frame, text="Добавить", command=add_workout)
    add_btn.grid(row=0, column=6, padx=10)

    # --- Фрейм фильтрации ---
    filter_frame = ttk.LabelFrame(root, text="Фильтр", padding=10)
    filter_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, sticky="w")
    filter_type_entry = ttk.Entry(filter_frame)
    filter_type_entry.grid(row=0, column=1, padx=5)

    ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=2, sticky="w")
    filter_date_entry = ttk.Entry(filter_frame)
    filter_date_entry.grid(row=0, column=3, padx=5)

    filter_btn = ttk.Button(filter_frame, text="Применить", command=apply_filter)
    filter_btn.grid(row=0, column=4, padx=5)

    reset_btn = ttk.Button(filter_frame, text="Сброс", command=reset_filter)
    reset_btn.grid(row=0, column=5, padx=5)

    # --- Таблица ---
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

    columns = ("ID", "Дата", "Тип", "Длительность (мин)")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    del_btn = ttk.Button(root, text="Удалить выбранное", command=delete_workout)
    del_btn.pack(pady=5)

if __name__ == "__main__":
    # 1. Загружаем данные
    load_data()
    
    # 2. Создаем окно
    root = tk.Tk()
    
    # 3. Строим интерфейс
    create_interface(root)
    
    # 4. Обновляем таблицу при старте
    refresh_table()
    
    # 5. Запускаем главный цикл
    root.mainloop()
