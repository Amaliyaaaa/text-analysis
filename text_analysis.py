import re
from difflib import SequenceMatcher
from tkinter import Tk, Label, Text, Button, Scrollbar, END, messagebox, Menu, Frame
import os
import sys


def process_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compare_texts(text1, text2):
    similarity = SequenceMatcher(None, text1, text2).ratio()
    return similarity * 100


def compare_lists(text1, text2):
    list1 = list(text1.split(" "))
    list2 = list(text2.split(" "))
    words = 0
    matches = 0
    for word in list1:
        if word != " ":
            words += 1
            if word in list2:
                matches += 1
    return (matches / words) * 100 if words > 0 else 0


def analyze_texts():
    text1 = process_text(script_text.get("1.0", END).strip())
    text2 = process_text(call_text.get("1.0", END).strip())

    if not text1 or not text2:
        messagebox.showerror("Ошибка", "Введите текст скрипта и звонка.")
        return

    similarity_percentage = compare_texts(text1, text2)
    intersection_percentage = compare_lists(text1, text2)

    result_label.config(
        text=f"Сходство текстов: {similarity_percentage:.2f}%\n"
             f"Пересечение слов: {intersection_percentage:.2f}%",
        fg="#1C3A57"  # Темно-голубой цвет для текста результата
    )


def show_help():
    help_text = (
        "Сходство текстов: отражает общую схожесть текстов.\n\n"
        "Пересечение слов: показывает, какой процент слов, зафиксированных в тексте 1, присутствует в тексте 2."
    )
    messagebox.showinfo("Справка", help_text)


def add_context_menu(text_widget):
    menu = Menu(text_widget, tearoff=0)
    menu.add_command(label="Копировать", command=lambda: text_widget.event_generate("<<Copy>>"))
    menu.add_command(label="Вырезать", command=lambda: text_widget.event_generate("<<Cut>>"))
    menu.add_command(label="Вставить", command=lambda: text_widget.event_generate("<<Paste>>"))
    menu.add_command(label="Выделить всё", command=lambda: text_widget.tag_add("sel", "1.0", "end"))
    text_widget.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))


# Создаем основное окно
root = Tk()
root.title("Сходство текстов")

# Устанавливаем иконку приложения
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Центрирование окна на экране
window_width = 600
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = (screen_width // 2) - (window_width // 2)
y_cordinate = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Верхняя панель
top_frame = Frame(root)
top_frame.pack(fill="x", pady=5)

# Добавляем кнопку справки
help_button = Button(top_frame, text="?", font=("Arial", 14), command=show_help, width=2)
help_button.pack(side="right", padx=10)

# Виджет для ввода скрипта звонка
Label(root, text="Текст 1:", font=("Arial", 12)).pack(pady=5)
script_frame = Frame(root)
script_frame.pack(fill="x", padx=10)

script_text = Text(script_frame, height=7, wrap="word")
script_scrollbar = Scrollbar(script_frame, command=script_text.yview)
script_text.configure(yscrollcommand=script_scrollbar.set)
script_text.pack(side="left", fill="x", expand=True)
script_scrollbar.pack(side="right", fill="y")

# Добавляем контекстное меню
add_context_menu(script_text)

# Виджет для ввода текста звонка
Label(root, text="Текст 2:", font=("Arial", 12)).pack(pady=5)
call_frame = Frame(root)
call_frame.pack(fill="x", padx=10)

call_text = Text(call_frame, height=7, wrap="word")
call_scrollbar = Scrollbar(call_frame, command=call_text.yview)
call_text.configure(yscrollcommand=call_scrollbar.set)
call_text.pack(side="left", fill="x", expand=True)
call_scrollbar.pack(side="right", fill="y")

# Добавляем контекстное меню
add_context_menu(call_text)

# Кнопка для анализа
analyze_button = Button(root, text="Анализировать", font=("Arial", 14), bg="#B0DFFA", command=analyze_texts)
analyze_button.pack(pady=10)

# Метка для отображения результата
result_label = Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Запуск приложения
root.mainloop()
