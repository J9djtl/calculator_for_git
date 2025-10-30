import tkinter as tk
from frontend import CalculatorGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Калькулятор")
    root.geometry("600x350")

    app = CalculatorGUI(root)

    root.mainloop()
