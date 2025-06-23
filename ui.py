from calculator import Calculator
import customtkinter as ctk
from customtkinter import CTkButton
from button_layout import ButtonLayout

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class UI(Calculator):
    def __init__(self, root):
        super().__init__(root)
        self._create_widgets(tab=ButtonLayout.tab_1(self))

    def _create_button(self, text, command, row, column):
        button = CTkButton(self.root, 
                           text=text, 
                           command=command, 
                           font=("Arial", 20, "bold"), 
                           width=70, 
                           height=70)
        button.grid(row=row, column=column, padx=10, pady=10)

    def _create_colored_button(self, text, command, row, column, color, hover_color):
        button = CTkButton(self.root, 
                           text=text, 
                           command=command, 
                           fg_color=color,
                           hover_color=hover_color,
                           font=("Arial", 20, "bold"), 
                           width=70, 
                           height=70)
        button.grid(row=row, column=column, padx=10, pady=10)
    def _create_widgets(self, tab: ButtonLayout):
        for i, (text, cmd) in enumerate(tab):
            if text in "0123456789.=":
                self._create_colored_button(text, cmd, row=i//4+1, column=i%4, color="#403d3a", hover_color="#292828")
            elif text in "+-*/C":
                self._create_colored_button(text, cmd, row=i//4+1, column=i%4, color="orange", hover_color="#cc7c04",)
            elif text in "()⌫":
                self._create_colored_button(text, cmd, row=i//4+1, column=i%4, color="#807d7a", hover_color="#63605d")
            else:
                self._create_button(text, cmd, row=i//4+1, column=i%4)