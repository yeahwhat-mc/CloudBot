from cloudbot import hook
import sympy

@hook.command('math', 'calc', 'ca')
def calc(text):
    """calc <query> -- Calculates <query> using sympy."""
    try:
        result = float(sympy.sympify(text))
        if abs(result - round(result)) < 0.001:
            return int(round(result))
        else:
            return round(result, 8)
    except:
        return "Could not compute"
