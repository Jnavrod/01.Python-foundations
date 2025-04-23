import os, json, copy
from datetime import datetime
from my_utils import *

cart = {}
total_amount = 0

try:
    with open("inventory.json", "r") as file:
        warehouse = json.load(file)
        backup_warehouse = copy.deepcopy(warehouse)
except FileNotFoundError:
    print("Error: File 'inventory.json' doesn't exist, check path")
except json.JSONDecodeError:
    print("Error: File 'inventory.json' has invalid format, check json")


def ask_option() -> None:
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
def show_catalogue() -> None:
    global warehouse
    print("""  🏪 Product list 🛒\n""")

    for code, info in warehouse.items():
        print(f'''     ✅ {code} : {info["name"]}
        💲 Price : {info["price"]}
        📦 Availability : {info["stock"]}
''')

def add_to_cart() -> None:
    global cart, warehouse
    frame("🏪 Adding products 🛒")

    while True:
        product_id = input("Write ID-Product: ").upper()
        if product_id in warehouse:
            break
        else:
            print("Id product not found")

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

    if product_id in cart:
        cart[product_id]["quantity"] += qty
    else:
        cart[product_id] = {
            "name": warehouse[product_id]["name"],
            "price": warehouse[product_id]["price"],
            "quantity": qty, 
            "subtotal": warehouse[product_id]["price"] * qty
        }

    warehouse[product_id]["stock"] -= qty

    frame(f'✅ Product: "{warehouse[product_id]["name"]}" added')

def remove_from_cart() -> None:
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

def blank_cart() -> None:
    global cart, total_amount, warehouse
    frame("🛒❌ Vaciar carrito")

    if cart == {}:
        frame("⚠️  Your cart is already empty")
        return

    while True:
        confirmation = input("""   Are you sure you want to remove
    all items? (Y/N): """).upper()
        if confirmation == "Y":
            cart = {}
            total_amount = 0
            warehouse = backup_warehouse
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
def show_cart() -> None:
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

def finish_order() -> None:
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

    with open("inventory.json", "w") as file:
        json.dump(warehouse, file, indent=4)

    sales_data = {
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "products": cart,
        "total": total_amount
    }

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

def process(option: str) -> None:
    commands = {
        "1" : show_catalogue, 
        "2" : add_to_cart,
        "3" : remove_from_cart,
        "4" : blank_cart,
        "5" : show_cart,
        "6" : finish_order
    }
    commands.get(option)()

def start_menu() -> None:
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