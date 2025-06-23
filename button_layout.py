from typing import Callable, List, Tuple
import math

class ButtonLayout:
    @staticmethod
    def tab_1(calculator):
        button_layout : List[Tuple[str, Callable]] = [
        # Special functions
        ('⌫', calculator.backward), 
        ('(', lambda: calculator.add_to_calculation('(')), 
        (')', lambda: calculator.add_to_calculation(')')),
        ('C', calculator.clear_field), 
        # Numbers and basic operators
        ('7', lambda: calculator.add_to_calculation(7)), ('8', lambda: calculator.add_to_calculation(8)), 
        ('9', lambda: calculator.add_to_calculation(9)), ('/', lambda: calculator.add_to_calculation('/')),
        ('4', lambda: calculator.add_to_calculation(4)), ('5', lambda: calculator.add_to_calculation(5)), 
        ('6', lambda: calculator.add_to_calculation(6)), ('*', lambda: calculator.add_to_calculation('*')),
        ('1', lambda: calculator.add_to_calculation(1)), ('2', lambda: calculator.add_to_calculation(2)), 
        ('3', lambda: calculator.add_to_calculation(3)), ('-', lambda: calculator.add_to_calculation('-')),
        ('.', lambda: calculator.add_to_calculation('.')), ('0', lambda: calculator.add_to_calculation(0)),
        ('=', calculator.evaluate_calculation), ('+', lambda: calculator.add_to_calculation('+')),
    
        # Scientific functions
        ('x²', lambda: calculator.direct_calculation('**2')), ('π', lambda: calculator.add_to_calculation(math.pi)),
        ('e', lambda: calculator.add_to_calculation(math.e)), ('√', lambda: calculator.direct_calculation('sqrt')),
        ('2nd', lambda: calculator.switch_tab()), ('log', lambda: calculator.direct_calculation('log')),
        ('sin', lambda: calculator.direct_calculation('sin')), ('cos', lambda: calculator.direct_calculation('cos'))
        ]
        return button_layout
    
    @staticmethod
    def tab_2(calculator):
        button_layout : List[Tuple[str, Callable]] = [
        # Special functions
        ('⌫', calculator.backward), 
        ('(', lambda: calculator.add_to_calculation('(')), 
        (')', lambda: calculator.add_to_calculation(')')),
        ('C', calculator.clear_field), 

        # Numbers and basic operators
        ('7', lambda: calculator.add_to_calculation(7)), ('8', lambda: calculator.add_to_calculation(8)), 
        ('9', lambda: calculator.add_to_calculation(9)), ('/', lambda: calculator.add_to_calculation('/')),
        ('4', lambda: calculator.add_to_calculation(4)), ('5', lambda: calculator.add_to_calculation(5)), 
        ('6', lambda: calculator.add_to_calculation(6)), ('*', lambda: calculator.add_to_calculation('*')),
        ('1', lambda: calculator.add_to_calculation(1)), ('2', lambda: calculator.add_to_calculation(2)), 
        ('3', lambda: calculator.add_to_calculation(3)), ('-', lambda: calculator.add_to_calculation('-')),
        ('.', lambda: calculator.add_to_calculation('.')), ('0', lambda: calculator.add_to_calculation(0)),
        ('=', calculator.evaluate_calculation), ('+', lambda: calculator.add_to_calculation('+')),
    
        # Scientific functions
        ('xʸ', lambda: calculator.x_pow_y()), ('π', lambda: calculator.add_to_calculation(math.pi)),
        ('e', lambda: calculator.add_to_calculation(math.e)), ('√', lambda: calculator.direct_calculation('sqrt')),
        ('2nd', lambda: calculator.switch_tab()), ('ln', lambda: calculator.direct_calculation('ln')),
        ('sin', lambda: calculator.direct_calculation('sin')), ('cos', lambda: calculator.direct_calculation('cos'))
        ]
        return button_layout