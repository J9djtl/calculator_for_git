import tkinter as tk
from frontend import build_interface

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Калькулятор")
    root.geometry("500x300")

    build_interface(root)

    root.mainloop()
