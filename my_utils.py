import os, time
from typing import Callable

def clean_console() -> None: 
    os.system("cls" if os.name == "nt" else "clear")

def function_frame(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print("""
╔════════════════════════════════╗
        """)
        func(*args, **kwargs)
        print("""
╚════════════════════════════════╝
    """)
    return wrapper

def frame(text: str) -> None:
    print(f"""
╔════════════════════════════════╗
   {text}
╚════════════════════════════════╝""")

@function_frame
def show_menu() -> None:
    menu = """  Commands:
     1. Ver catálogo
     2. Agregar producto al carrito
     3. Eliminar producto del carrito
     4. Vaciar carrito
     5. Mostrar carrito
     6. Finalizar compra
     7. Salir"""
    print(menu)

@function_frame
def welcome_message() -> None: 
    print("""  🏪✨ Welcome to Market""")

@function_frame
def goodbye_message() -> None:
    print("""
    ✨ Thank you for visiting!✨                           

    We truly appreciate your time 
    and trust. Your presence means 
    a lot to us.    
    
    🛍️ We hope you found exactly 
    what you were looking for! 🛒
""")

def counter_to_zero_from(seconds: int) -> None:
    for remain_seconds in range(seconds, 0, -1):
        print(f"   Restarting in {remain_seconds}")
        time.sleep(1)
    clean_console()