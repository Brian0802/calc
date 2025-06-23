from customtkinter import CTk, CTkTextbox
from tkinter import messagebox
import math
import logging
from typing import Optional, Union, Set

class Constants:
    PI = 'π'
    E = 'e'
    VALUES = {
        PI: math.pi,
        E: math.e
    }

class Calculator:
    MAX_DIGITS = 50
    OPERATORS = {'+', '-', '*', '/', '.'}

    def __init__(self, root: CTk):
        self.root = root
        self.calculation = ""
        self.tab = "tab1"
        self.used_constants: Set[str] = set()

        # for x_pow_y function
        self.base: Optional[float] = None
        self.operation: Optional[str] = None

        self.text_result = CTkTextbox(self.root, 
                             height=50, 
                             width=320, 
                             font=("Arial", 30, "bold"), 
                             bg_color="black",
                             state="disabled",
                             cursor="arrow"
                             )
        self.text_result.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

        self._handle_keypress()
        self.add_to_calculation(0)

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _handle_keypress(self):
        self.root.bind("<Key-Escape>", lambda event: self.exit())
        self.root.bind("<c>", lambda event: self.clear_field())
        self.root.bind("<Return>", lambda event: self.evaluate_calculation())
        self.root.bind("<BackSpace>", lambda event: self.backward())
        
        # Bind number keys
        for i in range(10):
            self.root.bind(str(i), lambda event, digit=i: self.add_to_calculation(digit))
        
        # Bind operator keys
        self.root.bind("+", lambda event: self.add_to_calculation("+"))
        self.root.bind("-", lambda event: self.add_to_calculation("-"))
        self.root.bind("*", lambda event: self.add_to_calculation("*"))
        self.root.bind("/", lambda event: self.add_to_calculation("/"))
        self.root.bind(".", lambda event: self.add_to_calculation("."))

    def update_display(self):
        self.text_result.configure(state="normal")
        self.text_result.delete(1.0, "end")
        self.text_result.insert(1.0, self.calculation)
        self.text_result.configure(state="disabled") 

    def switch_tab(self):
        from button_layout import ButtonLayout
        
        if self.tab == "tab1":
            self.tab = "tab2"
            self.clear_buttons()
            self._create_widgets(tab=ButtonLayout.tab_2(self))
        else:
            self.tab = "tab1"
            self.clear_buttons()
            self._create_widgets(tab=ButtonLayout.tab_1(self))
    
    def _validate_input(self, symbol: Union[str, int]) -> bool:
        if len(self.calculation) >= self.MAX_DIGITS:
            self.logger.warning("Maximum input length reached")
            return False
            
        if str(symbol) in self.OPERATORS:
            if not self.calculation or self.calculation[-1] in self.OPERATORS:
                return False
        
        if str(symbol) in Constants.VALUES:
            parts = [x for x in self.calculation.replace(Constants.PI, '#').replace(Constants.E, '#').split('#') 
                    if any(op in x for op in self.OPERATORS)]
            if str(symbol) in self.used_constants and parts:
                self.logger.warning(f"Constant {symbol} already used between operators")
                return False
            self.used_constants.add(str(symbol))
                
        return True
    
    def add_to_calculation(self, symbol: Union[str, int]) -> None:
        if not self._validate_input(symbol):
            return

        if self.calculation == "0":
            if str(symbol) == ".":
                self.calculation += str(symbol)  # Append "." to "0" giving "0."
            else:
                self.calculation = str(symbol)  # Replace "0" with new symbol
        else:
            self.calculation += str(symbol)
        
        self.update_display()

    def evaluate_calculation(self):
        if not self.calculation:
            return
            
        try:
            calc = self.calculation
            for const, value in Constants.VALUES.items():
                calc = calc.replace(const, str(value))
                
            if self.operation == 'pow' and self.base is not None:
                result = self.base ** float(calc)
                self.calculation = str(result)
                self.base = None
                self.operation = None
            else:
                result = eval(calc)
                self.calculation = str(result)
            
            self.used_constants.clear()
            self.update_display()
            
        except ZeroDivisionError:
            self.logger.error("Division by zero")
            messagebox.showerror("Error", "Cannot divide by zero")
            self.clear_field()
        except SyntaxError:
            self.logger.error("Syntax error in calculation")
            messagebox.showerror("Error", "Invalid syntax in calculation")
            self.clear_field()
        except Exception as e:
            self.logger.error(f"Calculation error: {str(e)}")
            messagebox.showerror("Error", f"Error in calculation: {str(e)}")
            self.clear_field()

    def direct_calculation(self, operation: str) -> None:
        if not self.calculation:
            return
            
        try:
            value = float(eval(self.calculation))
            result = {
                'sqrt': lambda x: math.sqrt(x),
                'log': lambda x: math.log10(x),
                'ln': lambda x: math.log(x),
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                '**2': lambda x: x ** 2
            }[operation](value)
            
            self.calculation = str(result)
            self.update_display()
            
        except (ValueError, KeyError, ZeroDivisionError) as e:
            self.logger.error(f"Operation error: {str(e)}")
            self.clear_field()
            messagebox.showwarning("Error", f"Invalid operation: {str(e)}")

    def x_pow_y(self):
        if self.calculation:
            self.base = float(self.calculation)
            self.calculation = ''
            self.text_result.configure(state="normal")
            self.text_result.delete(1.0, "end")
            self.text_result.configure(state="disabled")
            self.operation = 'pow'
            return True

    def backward(self):
        if self.calculation is not None and self.calculation != "0":
            if len(self.calculation) == 1:
                self.calculation = self.calculation[:-1]
                self.add_to_calculation(0)
            else:
                self.calculation = self.calculation[:-1]
            self.update_display()

    def clear_buttons(self):
        # Remove all the buttons expect text_result
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

    def clear_field(self):
        self.calculation = ""
        self.add_to_calculation(0)
        self.base = None
        self.operation = None
        self.used_constants.clear()
        self.update_display()
    
    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()