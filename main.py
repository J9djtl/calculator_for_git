import tkinter as tk
from frontend import CalculatorGUI
from memory import CalculatorMemory

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Калькулятор")
    root.geometry("600x350")

    memory = CalculatorMemory()
    app = CalculatorGUI(root, memory)

    root.mainloop()
