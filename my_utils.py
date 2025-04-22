import os, time

def clean_console(): #Done
    os.system("cls" if os.name == "nt" else "clear")

def function_frame(func): #Done
    def wrapper(*args, **kwargs):
        print("""
╔════════════════════════════════╗
        """)
        func(*args, **kwargs)
        print("""
╚════════════════════════════════╝
    """)
    return wrapper

def frame(text): #Done
    print(f"""
╔════════════════════════════════╗
   {text}
╚════════════════════════════════╝""")

@function_frame
def show_menu(): #Done
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
def welcome_message(): #Done
    print("""  🏪✨ Welcome to Market""")

@function_frame
def goodbye_message(): #Done
    print("""
    ✨ Thank you for visiting!✨                           

    We truly appreciate your time 
    and trust. Your presence means 
    a lot to us.    
    
    🛍️ We hope you found exactly 
    what you were looking for! 🛒
""")

def counter_to_zero_from(seconds):
    for remain_seconds in range(seconds, 0, -1):
        print(f"   Restanting in {remain_seconds}")
        time.sleep(1)
    clean_console()