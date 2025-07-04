import customtkinter as ctk
from calculator import Calculator

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Calculator")
    root.geometry("360x720")
    root.resizable(False,False)
    root.config(bg="black")
    root.iconbitmap("calc.ico")
    app = Calculator(root)
    root.mainloop()