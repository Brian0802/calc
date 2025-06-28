from customtkinter import CTk, CTkTextbox, CTkButton
from tkinter import messagebox
import math
import logging
import re
from typing import Optional, Union, Set
from button_layout import ButtonLayout

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
        self._create_widgets(tab=ButtonLayout.tab_1(self))
        self.used_constants: Set[str] = set()

        # for x_pow_y function
        self.base: Optional[float] = None
        self.operation: Optional[str] = None
        self.pending_operation_display = ""

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
        self.root.bind("<C>", lambda event: self.clear_field())  # Both cases
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
        
        # Additional useful bindings
        self.root.bind("<KeyPress-equal>", lambda event: self.evaluate_calculation())

    def update_display(self):
        self.text_result.configure(state="normal")
        self.text_result.delete(1.0, "end")
        
        display_text = self.calculation
        if self.pending_operation_display:
            display_text = f"{self.pending_operation_display} {display_text}"
            
        self.text_result.insert(1.0, display_text)
        self.text_result.configure(state="disabled") 

    def switch_tab(self):
        try:
            from button_layout import ButtonLayout
            
            if self.tab == "tab1":
                self.tab = "tab2"
                self.clear_buttons()
                self._create_widgets(ButtonLayout.tab_2(self))
            else:
                self.tab = "tab1"
                self.clear_buttons()
                self._create_widgets(ButtonLayout.tab_1(self))
        except ImportError:
            self.logger.error("ButtonLayout module not found")
            messagebox.showerror("Error", "Button layout module not available")
    
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
    
    def _validate_input(self, symbol: Union[str, int]) -> bool:
        """Improved input validation"""
        symbol_str = str(symbol)
        
        # Check maximum length
        if len(self.calculation) >= self.MAX_DIGITS:
            self.logger.warning("Maximum input length reached")
            messagebox.showwarning("Warning", f"Maximum {self.MAX_DIGITS} digits allowed")
            return False
        
        # Validate operators
        if symbol_str in self.OPERATORS:
            if not self.calculation or self.calculation[-1] in self.OPERATORS:
                if symbol_str != '.' or self.calculation[-1:] == '.':
                    return False
        
        # Validate decimal points
        if symbol_str == '.':
            # Check if current number already has a decimal point
            parts = re.split(r'[+\-*/]', self.calculation)
            if parts and '.' in parts[-1]:
                return False
        
        # Validate constants (improved logic)
        if symbol_str in Constants.VALUES:
            # Reset constant tracking after operators
            current_term = re.split(r'[+\-*/]', self.calculation)[-1] if self.calculation else ""
            if symbol_str in current_term:
                self.logger.warning(f"Constant {symbol_str} already used in current term")
                return False
                
        return True
    
    def add_to_calculation(self, symbol: Union[str, int]) -> None:
        if not self._validate_input(symbol):
            return

        symbol_str = str(symbol)
        
        if self.calculation == "0":
            if symbol_str == ".":
                self.calculation += symbol_str  # Append "." to "0" giving "0."
            elif symbol_str.isdigit():
                self.calculation = symbol_str  # Replace "0" with new digit
            else:
                self.calculation += symbol_str  # For operators and constants
        else:
            self.calculation += symbol_str
        
        self.update_display()

    def safe_evaluate(self, expression: str) -> float:
        """Safer evaluation method to replace eval()"""
        try:
            # Replace constants with their values
            for const, value in Constants.VALUES.items():
                expression = expression.replace(const, str(value))
            
            # Basic validation - only allow numbers, operators, and parentheses
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters in expression")
            
            # Use eval with restricted globals for basic safety
            # In production, consider using a proper expression parser
            allowed_names = {
                "__builtins__": {},
                "__name__": "__main__",
                "__doc__": None,
            }
            
            return float(eval(expression, allowed_names, {}))
            
        except Exception as e:
            raise ValueError(f"Cannot evaluate expression: {str(e)}")

    def evaluate_calculation(self):
        if not self.calculation:
            return
            
        try:
            if self.operation == 'pow' and self.base is not None:
                exponent = self.safe_evaluate(self.calculation)
                result = self.base ** exponent
                self.calculation = self._format_result(result)
                self.base = None
                self.operation = None
                self.pending_operation_display = ""
            else:
                result = self.safe_evaluate(self.calculation)
                self.calculation = self._format_result(result)
            
            self.used_constants.clear()
            self.update_display()
            
        except ZeroDivisionError:
            self.logger.error("Division by zero")
            messagebox.showerror("Error", "Cannot divide by zero")
            self.clear_field()
        except ValueError as e:
            self.logger.error(f"Value error: {str(e)}")
            messagebox.showerror("Error", f"Invalid calculation: {str(e)}")
            self.clear_field()
        except Exception as e:
            self.logger.error(f"Calculation error: {str(e)}")
            messagebox.showerror("Error", f"Error in calculation: {str(e)}")
            self.clear_field()

    def _format_result(self, result: float) -> str:
        """Format the result to avoid unnecessary decimal places"""
        if result.is_integer():
            return str(int(result))
        else:
            # Round to reasonable precision
            formatted = f"{result:.10f}".rstrip('0').rstrip('.')
            return formatted

    def direct_calculation(self, operation: str) -> None:
        if not self.calculation:
            return
            
        try:
            value = self.safe_evaluate(self.calculation)
            
            # Validate operations
            if operation in ['sqrt', 'log', 'ln'] and value < 0:
                raise ValueError(f"Cannot perform {operation} on negative number")
            
            if operation == 'log' and value == 0:
                raise ValueError("Cannot take log of zero")
                
            if operation == 'ln' and value == 0:
                raise ValueError("Cannot take natural log of zero")
            
            result = {
                'sqrt': lambda x: math.sqrt(x),
                'log': lambda x: math.log10(x),
                'ln': lambda x: math.log(x),
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                '**2': lambda x: x ** 2,
                'factorial': lambda x: math.factorial(int(x)) if x >= 0 and x == int(x) else None,
                '1/x': lambda x: 1/x if x != 0 else None
            }[operation](value)
            
            if result is None:
                raise ValueError(f"Invalid operation {operation} for value {value}")
            
            self.calculation = self._format_result(result)
            self.update_display()
            
        except (ValueError, KeyError, ZeroDivisionError, OverflowError) as e:
            self.logger.error(f"Operation error: {str(e)}")
            messagebox.showerror("Error", f"Invalid operation: {str(e)}")
            self.clear_field()

    def x_pow_y(self):
        """Improved power function with visual feedback"""
        if self.calculation:
            try:
                self.base = self.safe_evaluate(self.calculation)
                self.pending_operation_display = f"{self.calculation}^"
                self.calculation = ''
                self.operation = 'pow'
                self.update_display()
                return True
            except Exception as e:
                self.logger.error(f"Power operation error: {str(e)}")
                messagebox.showerror("Error", "Invalid base for power operation")
                return False
        return False

    def backward(self):
        """Improved backspace functionality"""
        if self.calculation and self.calculation != "0":
            if len(self.calculation) == 1:
                self.calculation = "0"
            else:
                self.calculation = self.calculation[:-1]
                # If we removed all characters, default to 0
                if not self.calculation:
                    self.calculation = "0"
            self.update_display()

    def clear_buttons(self):
        """Remove all buttons except text_result"""
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

    def clear_field(self):
        """Clear all calculations and reset state"""
        self.calculation = "0"
        self.base = None
        self.operation = None
        self.pending_operation_display = ""
        self.used_constants.clear()
        self.update_display()
    
    def exit(self):
        """Safe exit with confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()  # Use quit() instead of destroy() for cleaner exit
            self.root.destroy()

    def get_calculation_history(self):
        """Method to get calculation history - can be extended"""
        # This could be implemented to store and retrieve calculation history
        pass

    def memory_functions(self, operation: str, value: Optional[float] = None):
        """Memory functions - can be extended"""
        # This could be implemented for memory store/recall functionality
        pass