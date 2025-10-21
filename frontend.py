from tkinter import *
from tkinter import ttk

def build_interface(root):
    frame_top = ttk.Frame(root)
    frame_top.pack(pady=10)

    label = ttk.Label(frame_top, text="Это наш калькулятор")
    label.pack(anchor='e')

    entry = ttk.Entry(frame_top)
    entry.pack(anchor='center', padx=8, pady=8)

    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(pady=10)

    def on_click(char):
        current = entry.get()
        entry.delete(0, END)
        entry.insert(0, current + char)

    def on_equal_press():
        expression = entry.get()
        try:
            result = str(eval(expression))  # временно
        except Exception:
            result = "Ошибка"
        entry.delete(0, END)
        entry.insert(0, result)

    def on_clear():
        entry.delete(0, END)

    buttons = [
        '', '', '', 'C',
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '.', '0', '=', '+',
    ]

    n_cols = 4
    for index, char in enumerate(buttons):
        row = index // n_cols
        col = index % n_cols

        if char == '=':
            cmd = on_equal_press
        elif char == 'C':
            cmd = on_clear
        else:
            cmd = lambda t=char: on_click(t)

        btn = ttk.Button(frame_buttons, text=char, command=cmd)
        btn.grid(row=row, column=col, padx=5, pady=5)
