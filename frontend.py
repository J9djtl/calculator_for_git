from tkinter import *
from tkinter import ttk
from logic import evaluate_expression

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.n_cols = 4

        self.frame_top = ttk.Frame(root)
        self.frame_top.pack(pady=10)

        self.label = ttk.Label(self.frame_top, text="Это наш калькулятор")
        self.label.pack(anchor='ne')

        self.entry = ttk.Entry(self.frame_top)
        self.entry.pack(anchor='center', padx=8, pady=8)

        self.frame_buttons = ttk.Frame(root)
        self.frame_buttons.pack(pady=10)

        self.buttons = [
            '', '', '', 'C',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', '=', '+',
        ]

        self.render_buttons()

    def on_button_click(self, char):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, current + char)

    def on_equal_press(self):
        expression = self.entry.get()
        try:
            result = str(eval(expression))  # временно, сюда evaluate_expression()
        except Exception:
            result = "Ошибка"
        self.entry.delete(0, END)
        self.entry.insert(0, result)

    def on_clear(self):
        self.entry.delete(0, END)

    def render_buttons(self):
        for index, char in enumerate(self.buttons):
            row = index // self.n_cols
            col = index % self.n_cols

            if char == '=':
                cmd = self.on_equal_press
            elif char == 'C':
                cmd = self.on_clear
            else:
                cmd = lambda t=char: self.on_button_click(t)

            btn = ttk.Button(self.frame_buttons, text=char, command=cmd)
            btn.grid(row=row, column=col, padx=5, pady=5)
