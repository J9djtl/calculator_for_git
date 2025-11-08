from tkinter import *

from tkinter import ttk
from logic import evaluate_expression

class CalculatorGUI:
    def __init__(self, root, memory):
        self.root = root
        # self.root.iconbitmap('assets/calc.ico')  # для .ico на Windows
        icon_image = PhotoImage(file='assets/calc.png')
        root.iconphoto(True, icon_image) 
        self.memory = memory

        self.frame_top = ttk.Frame(root)
        self.frame_top.pack(pady=10)


        self.entry = Text(self.frame_top, height=2, width=30, font=('Arial', 16), state='disabled')
        self.entry.pack(anchor='center', padx=8, pady=8)


        self.frame_buttons = ttk.Frame(root)
        self.frame_buttons.pack(pady=10)

        self.n_cols = 6
        self.buttons = [
            'MC', 'MR', 'MS', 'M+', 'M−', 'ANS',       
            '(', ')', 'C', '⌫', '%',  'AC',           
            '7', '8', '9', '/', 'sqrt', 'sin',          
            '4', '5', '6', '*', '^', 'cos',         
            '1', '2', '3', '-', '1/x', 'floor',           
            '.', '0', '=', '+', '10ˣ', 'ceil'           
        ]

        style = ttk.Style()
        style.configure('Basic.TButton', background='#e0f7fa')
        style.configure('Extended.TButton', background='#ffe0b2')
        style.configure('Memory.TButton', background='#f8bbd0')

        self.render_buttons()

        self.frame_message = ttk.Frame(root)
        self.frame_message.pack(pady=(5, 10))

        self.message_label = ttk.Label(self.frame_message, text="", font=('Arial', 10))
        self.message_label.pack()
        self.message_label.pack_forget()


    def get_text(self):
        return self.entry.get('1.0', 'end-1c')
    
    def set_text(self, value):
        self.entry.configure(state='normal')
        self.entry.delete('1.0', END)
        self.entry.insert('1.0', value)
        self.entry.configure(state='disabled')

    def append_text(self, value):
        self.entry.configure(state='normal')
        self.entry.insert(END, value)
        self.entry.configure(state='disabled')

    def show_message(self, text, color="#10349F"):
        self.message_label.configure(text=text, foreground=color)
        self.message_label.pack()

    def hide_message(self):
        self.message_label.pack_forget()


    def on_button_click(self, char):
        self.hide_message()
        self.append_text(char)

    def on_equal_press(self):
        self.hide_message()
        expression = self.get_text()
        try:
            result = str(evaluate_expression(expression))
        except Exception:
            result = "Ошибка"
        self.set_text(result)

    def on_clear(self):
        self.hide_message()
        self.set_text("")

    def on_backspace(self):
        self.hide_message()
        current = self.get_text()
        self.set_text(current[:-1])

    def on_memory_stub(self):
        self.show_message("Функции памяти пока не реализованы")


    def on_all_clear(self):
        self.hide_message()
        self.set_text("")
        # Здесь можно добавить сброс памяти, истории и т.д.

    def on_insert_function(self, func_name):
        self.hide_message()
        self.append_text(func_name + '(')

    def on_insert_special(self, pattern):
        self.hide_message()
        self.append_text(pattern)

    def on_memory_clear(self):
        """Очищает значение памяти"""
        self.memory.clear()
        self.show_message("Память очищена")

    def on_memory_recall(self):
        """Извлекает значение из памяти и отображает его"""
        value = self.memory.get()
        self.append_text(value)

    def on_memory_store(self):
        """Сохраняет текущее выражение в память"""
        try:
            self.memory.store(self.get_text())
            value = self.get_text()
            self.show_message(f"Сохранено: {value}")
        except Exception:
            self.show_message('Ошибка при сохранении в память')

    def on_memory_add(self):
        """Добавляет текущее значение к памяти"""
        try:
            self.memory.add(self.get_text())
            value = self.get_text()
            self.show_message(f"Добавлено к памяти: {value}")
        except Exception:
            self.show_message('Ошибка при добавлении значения к памяти')

    def on_memory_subtract(self):
        """Вычитает текущее значение из памяти"""
        try:
            self.memory.subtract(self.get_text())
            value = self.get_text()
            self.show_message(f"Вычтено из памяти: {value}")
        except Exception:
            self.show_message('Ошибка при вычитании значения из памяти')

    def get_button_type(self, char, index):
        # Память
        if char in {'MC', 'MR', 'MS', 'M+', 'M−', 'ANS', 'AC'}:
            return 'memory'
        # Расширенные операции (последние 2 колонки)
        elif index % self.n_cols >= 4:
            return 'extended'
        # Базовые элементы (цифры, операторы, скобки)
        else:
            return 'basic'
        

    def get_button_command(self, char):
        memory_commands = {
            'MC': self.on_memory_clear,
            'MR': self.on_memory_recall,
            'MS': self.on_memory_store,
            'M+': self.on_memory_add,
            'M−': self.on_memory_subtract
        }

        special_commands = {
            '=': self.on_equal_press,
            'C': self.on_clear,
            '⌫': self.on_backspace,
            'AC': self.on_all_clear,
            '1/x': lambda: self.on_button_click('1/('),
            '10ˣ': lambda: self.on_button_click('10^('),
            'ANS': lambda: self.on_button_click('ANS')
        }

        function_commands = {f: lambda f=f: self.on_button_click(f + '(')
                            for f in ['sqrt', 'sin', 'cos', 'floor', 'ceil']}

        if char in memory_commands:
            return memory_commands[char]
        elif char in special_commands:
            return special_commands[char]
        elif char in function_commands:
            return function_commands[char]
        else:
            return lambda: self.on_button_click(char)



    def render_buttons(self):
        for index, char in enumerate(self.buttons):
            row = index // self.n_cols
            col = index % self.n_cols

            cmd = self.get_button_command(char)

            btn_type = self.get_button_type(char, index)
            style_map = {
                'basic': 'Basic.TButton',
                'extended': 'Extended.TButton',
                'memory': 'Memory.TButton'
            }

            btn = ttk.Button(self.frame_buttons, text=char, command=cmd, style=style_map[btn_type])
            btn.grid(row=row, column=col, padx=5, pady=5)
