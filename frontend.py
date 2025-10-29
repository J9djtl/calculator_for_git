from tkinter import *
from tkinter import ttk
from logic import evaluate_expression

class CalculatorGUI:
    def __init__(self, root):
        self.root = root


        self.frame_top = ttk.Frame(root)
        self.frame_top.pack(pady=10)

        self.label = ttk.Label(self.frame_top, text="Это наш калькулятор")
        self.label.pack(anchor='ne')

        self.entry = ttk.Entry(self.frame_top)
        self.entry.pack(anchor='center', padx=8, pady=8)

        self.frame_buttons = ttk.Frame(root)
        self.frame_buttons.pack(pady=10)

        self.n_cols = 6
        self.buttons = [
            'MC', 'MR', 'MS', 'M+', 'M−', 'AС',       
            '(', ')', 'C', '⌫', '%',  'ANS',           
            '7', '8', '9', '/', 'sqrt', 'sin',          
            '4', '5', '6', '*', '^', 'cos',         
            '1', '2', '3', '-', '1/x', 'floor',           
            '.', '0', '=', '+', '10ˣ', 'ceil'           
        ]


        self.render_buttons()

    def on_button_click(self, char):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, current + char)

    def on_equal_press(self):
        expression = self.entry.get()
        try:
            result = str(evaluate_expression(expression))
        except Exception:
            result = "Ошибка"
        self.entry.delete(0, END)
        self.entry.insert(0, result)

    def on_clear(self):
        self.entry.delete(0, END)

    def on_backspace(self):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, current[:-1])

    def on_memory_stub(self):
        print("Функции памяти пока не реализованы")

    def on_all_clear(self):
        self.entry.delete(0, END)
        # Здесь можно добавить сброс памяти, истории и т.д.

    def on_insert_function(self, func_name):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, current + func_name + '(')

    def on_insert_special(self, pattern):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, current + pattern)




    def render_buttons(self):
        for index, char in enumerate(self.buttons):
            row = index // self.n_cols
            col = index % self.n_cols

            if char == '=':
                cmd = self.on_equal_press
            elif char == 'C':
                cmd = self.on_clear
            elif char == '⌫':
                cmd = self.on_backspace
            elif char == 'AC':
                cmd = self.on_all_clear
            elif char == '1/x':
                cmd = lambda: self.on_button_click('1/(')
            elif char == '10ˣ':
                cmd = lambda: self.on_button_click('10^(')
            elif char in {'sqrt', 'sin', 'cos', 'floor', 'ceil'}:
                cmd = lambda t=char: self.on_button_click(t + '(')
            elif char in {'MC', 'MR', 'MS', 'M+', 'M−', 'ANS'}:
                cmd = self.on_memory_stub
            elif char == '':
                pass  # пропускаем пустую кнопку
            else:
                cmd = lambda t=char: self.on_button_click(t)

            btn = ttk.Button(self.frame_buttons, text=char, command=cmd)
            btn.grid(row=row, column=col, padx=5, pady=5)
