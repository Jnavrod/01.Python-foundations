import os, json, time
from datetime import datetime

#Initializing the cart and total value
cart = {}
total_amount = 0

#Getting current inventory
try:
    with open("inventory.json", "r") as file:
        warehouse = json.load(file)
        backup_warehouse = warehouse #Doing a backup if needed
except FileNotFoundError:
    print("Error: File 'inventory.json' doesn't exist, check path")
except json.JSONDecodeError:
    print("Error: File 'inventory.json' has invalid format, check json")

#Some extra and not relevant features
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

# Relevant functions in main menu
def ask_option(): #Done
    while True:
        show_menu()
        option = input("Option: ")
        av_options = ["1", "2", "3", "4", "5", "6", "7"]
    
        if option in av_options:
            clean_console()
            return option
        else:
            print("Last error: Not valid option, type option number.")
            clean_console()

@function_frame
def show_catalogue(): #Done
    global warehouse
    print("""  🏪 Product list 🛒\n""")

    for code, info in warehouse.items():
        print(f'''     ✅ {code} : {info["name"]}
        💲 Price : {info["price"]}
        📦 Availability : {info["stock"]}
''')

def add_to_cart(): #Done
    global cart, warehouse
    frame("🏪 Adding products 🛒")

    # Ask and valid ID
    while True:
        product_id = input("Write ID-Product: ").upper()
        if product_id in warehouse:
            break
        else:
            print("Id product not found")

    # Ask and valid quantity
    while True:
        stock = warehouse[product_id]["stock"]
        try:
            qty = input("Enter the quantity: ")

            if not qty.isdigit():
                raise ValueError("❌ Please enter a valid number.")

            qty = int(qty)

            if str(qty).isdigit() and qty != 0:
                if qty <= stock:
                    break
                else:
                    print(f'There is not enough stock, ({stock} units) at warehouse, try again')
            else:
                print("Enter a positive valid integer number")
        
        except ValueError as e:
            print(e)

    # Add to the cart
    if product_id in cart:
        cart[product_id]["quantity"] += qty
    else:
        cart[product_id] = {
            "name": warehouse[product_id]["name"],
            "price": warehouse[product_id]["price"],
            "quantity": qty, 
            "subtotal": warehouse[product_id]["price"] * qty
        }

    # Update warehouse stock
    warehouse[product_id]["stock"] -= qty

    # Feedback to customer
    frame("✅ Product added")

def remove_from_cart(): #Done
    global total_amount
    frame("🚮 Remove all items 🗑️")
    while True:
        product_id = input("Write ID-Product: ").upper()

        if product_id in cart:
            cart_info = cart[product_id]
            if product_id in warehouse:
                warehouse_info = warehouse[product_id]
                warehouse_info["stock"] += cart_info["quantity"]

            total_amount -= cart[product_id]["subtotal"]
            del cart[product_id]
            frame(f"""✅ Product {cart_info["name"]}
        Successfully removed""")
            break
            
        else:
            frame("🤔 Product-ID not found")

def blank_cart(): #Done
    global cart, total_amount
    frame("🛒❌ Vaciar carrito")
    while True:
        confirmation = input("""   Are you sure you want to remove
    all items? (Y/N): """).upper()
        if confirmation == "Y":
            cart = {}
            total_amount = 0
            frame("🚮 Your cart is now empty 🧹")
            return
        elif confirmation =="N":
            frame("❌ Operation cancelled 🔙")
            counter_to_zero_from(2)
            return
        else:
            frame("""❌ That's not a valid input
       Just write "Y" or "N""")

@function_frame
def show_cart(): #Done
    global total_amount
    total_amount = 0
    print("       🛒   Shopping cart  🛒 \n")
    if cart == {}:
        print("     Cart is empty")
        return

    for code, info in cart.items():
        subtotal = info["price"] * info["quantity"]
        info["subtotal"] = subtotal
        total_amount += info["subtotal"]
        print(f'''     ✅ {code} : {info["name"]}
        💲 Price : {info["price"]}
        📦 Quantity : {info["quantity"]}
        💲 Subtotal : {info["subtotal"]}
''')

    frame(f"Total Order amount: {total_amount}")


def finish_order(): #Done
    global cart
    show_cart()
    frame("Buying process form")
    if not cart or len(cart) == 0:
        frame("""❔ Sorry, your cart is empty.
    Insert some items 🔙""")
        counter_to_zero_from(3)
        return
    while True:
        confirmation = input(""" Please confirm  payment
       Do you proceed to pay? (Y/N): """).upper()
        if confirmation == "Y":
            frame("✅ Successfully payed! 💳🎉")
            break
        elif confirmation =="N":
            frame("❌ Operation cancelled 🔙")
            counter_to_zero_from(2)
            return
        else:
            frame("""❌ That's not a valid input
       Just write "Y" or "N""")

    #Inventory updating process (Not really the best way)
    with open("inventory.json", "w") as file:
        json.dump(warehouse, file, indent=4)

    #Data to be sent ot the txt
    sales_data = {
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "products": cart,
        "total": total_amount
    }

    #Save orders in a txt
    historic = "sales_historic.txt"
    if not os.path.exists(historic):
        with open(historic, "w") as file:
            file.write("")
    
    with open(historic, "r+") as file:
        file.seek(0, os.SEEK_END)
        file.write(json.dumps(sales_data, indent=4) + "\n")
    
    cart = {}
    counter_to_zero_from(3)
    return

def process(option): #Done
    commands = {
        "1" : show_catalogue, 
        "2" : add_to_cart,
        "3" : remove_from_cart,
        "4" : blank_cart,
        "5" : show_cart,
        "6" : finish_order
    }
    commands.get(option)()

def start_menu(): #Done
    option = 0
    clean_console()
    welcome_message()
    while option != "7":
        option = ask_option()
        if option == "7":
            goodbye_message()
            return
        process(option)

start_menu()