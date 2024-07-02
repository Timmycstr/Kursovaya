import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("База недвижимости")

        # Данные будут храниться в списке
        self.properties = []

        # Создание интерфейса
        self.create_widgets()
        # Загрузка данных из базы данных SQLite
        self.load_data_from_db("properties.db")

    def create_widgets(self):
        # Фрейм для формы добавления недвижимости
        form_frame = ttk.LabelFrame(self.root, text="Добавить недвижимость")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Поля формы
        fields = [
           "Тип объекта", 
            "Площадь", "Адрес", 
            "Цена", "ФИО клиента"
        ]
        self.entries = {}
        for i, field in enumerate(fields):
            label = ttk.Label(form_frame, text=field)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[field] = entry

        # Кнопка для добавления недвижимости
        add_button = ttk.Button(form_frame, text="Добавить", command=self.add_property)
        add_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

        # Таблица для отображения недвижимости
        self.tree = ttk.Treeview(self.root, columns=fields, show="headings")
        for field in fields:
            self.tree.heading(field, text=field, command=lambda col=field: self.sort_column(col, False))
            self.tree.column(field, width=100)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Горизонтальный и вертикальный скроллбары
        scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscroll=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        scrollbar_x.grid(row=2, column=0, sticky="ew")
        self.tree.configure(xscroll=scrollbar_x.set)

        # Обработчики событий для заголовков столбцов для сортировки
        for col in fields:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))

    def sort_column(self, col, reverse):
        try:
            data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
            data.sort(reverse=reverse)
            for i, item in enumerate(data):
                self.tree.move(item[1], '', i)
            self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
        except Exception as e:
            print(e)

    def add_property(self):
        property_data = {field: entry.get() for field, entry in self.entries.items()}
        
        if any(not value for value in property_data.values()):
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля")
            return

        self.properties.append(property_data)
        self.tree.insert("", "end", values=tuple(property_data.values()))

        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def load_data_from_db(self, db_filename):
        try:
            # Проверка пути и файла
            current_directory = os.getcwd()
            db_path = os.path.join(current_directory, db_filename)
            print(f"Попытка загрузить данные из базы данных: {db_path}")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM properties")
            rows = cursor.fetchall()

            for row in rows:
                property_data_dict = {
                    "Тип объекта": row[0],
                    "Площадь": row[1],
                    "Адрес": row[2 and 3],
                    "Цена": row[4],
                    "ФИО клиента": row[5]
                }
                self.properties.append(property_data_dict)
                self.tree.insert("", "end", values=tuple(property_data_dict.values()))

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при работе с базой данных: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
