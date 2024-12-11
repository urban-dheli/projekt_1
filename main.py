'''
main.py: filen som innehåller alla funktioner som får programmet att fungera

__author__  = "Alfred Lundström"
__version__ = "1.0.0"
__email__   = "alfred.lundstrom@ga.ntig.se"
'''

import csv
import os
import locale
from time import sleep
import uuid

def load_data(filename): 
    products = [] 
    
    with open(filename, 'r', encoding="UTF-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(
                {
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def add_products(products, name, desc, price, quantity): # lägger till produkt i products och csv

    max_id = max(products, key = lambda x: x['id'])
    new_id = max_id['id'] + 1

    new_product = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }

    products.append(new_product)

    with open('products.csv', 'a') as fd:
        fd.write(f"\n{new_id},{name},{desc},{price},{quantity}")

    return f"Du la till produkt {name} med id: {new_id}"

def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break

    if temp_product:
        products.remove(temp_product)

        with open('products.csv', 'w', newline='') as file:
            fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for product in products:
                writer.writerow(product)
        
        return f"Produkt med id: {id + 1} har tagits bort"
    else:
        return f"Produkt med id: {id + 1} hittades inte"

def edit_product(products, id, name, desc, price, quantity):
    edit = None

    for product in products:
        if product['id'] == id:
            edit = product
            break

    if edit != None:
        edit['name'] = name
        edit['desc'] = desc
        edit['price'] = price
        edit['quantity'] = quantity

        with open('products.csv', 'w', newline = '') as file:
            fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            
            writer.writeheader()

            for product in products:
                writer.writerow(product)

        return f"Produkt med id: {id + 1} har ändrats"
    
    return f"Produkt med id: {id + 1} hittades inte"

def total_product_worth(products):
    total_worth = sum(product['price'] * product['quantity'] for product in products)
    return f"{bcolors.PURPLE}Totalt värde på alla produkter i lagret: {locale.currency(total_worth, grouping = True)}{bcolors.DEFAULT}"

def view_product(products, id):
    for product in products:
        if product["id"] == id:
            return f"{bcolors.RED}Visar produkt: {bcolors.DEFAULT}{product['name']}" \
                f"\n{bcolors.RED}Beskrivning: {bcolors.DEFAULT}{product['desc']}" \
                    f"\n{bcolors.RED}ID: {bcolors.DEFAULT}{product['id']}"
    
    return "Produkten hittas inte"

def view_products(products):
    product_list = []
    name_width = 25
    desc_width = 45
    price_width = 5

    header = f"{bcolors.PURPLE}{'Id':<6} {'Name':<{name_width}}" \
        f"{'Description':<{desc_width}} {'Price':>{price_width}}"
    product_list.append(header)

    product_list.append(f"{bcolors.CYAN}_______________________________________________________________________________________\n")

    for index, product in enumerate(products, 1):
        name = product['name'] if len(product['name']) <= 15 else product['name'][:15] + "..."
        desc = product['desc'] if len(product['desc']) <= 30 else product['desc'][:30] + "..."
        
        product_info = f"{bcolors.DEFAULT}{index:<5} {name:<{name_width}} {desc:<{desc_width}}" \
             f"{locale.currency(product['price'], grouping=True):>{price_width}}"
        product_list.append(product_info)

    product_list.append(f"{bcolors.CYAN}_______________________________________________________________________________________\n")
    total_value = total_product_worth(products)
    product_list.append(total_value)
    
    return "\n".join(product_list)

def get_product(products, id):
    for product in products:
        if product["id"] == id:
            return product
        
    return "Produkten finns ej"

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('products.csv')
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))

        choice = input(f"{bcolors.RED}\n(L)ägg till \n(Ä)ndra \n(V)isa \n(T)a bort" \
            f"\n{bcolors.DEFAULT}").strip().upper()

        if choice == "L":
            os.system('cls' if os.name == 'nt' else 'clear')

            print(f"{bcolors.RED}Ny produkt:{bcolors.DEFAULT}\n")

            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))

            print(add_products(products, name, desc, price, quantity))
            sleep(1)

        elif choice in ["Ä", "V", "T"]:

            try:
                index = int(input("Enter product ID: "))

            except ValueError:
                print("Välj produkt-id med siffror")
                sleep(1)
                continue

            if 1 <= index <= len(products):
                selected_product = products[index - 1]
                id = selected_product['id']

            if choice == "Ä":
                os.system('cls' if os.name == 'nt' else 'clear')

                placeholder = get_product(products, id)

                print(f"{bcolors.RED}Du redigerar nu produkt med ID {bcolors.DEFAULT}{id}\n")

                name = input(f"Ändra namn: ({placeholder['name']})   ").strip()
                if not name:
                    name = placeholder['name']

                desc = input(f"Ändra beskrivningen: ({placeholder['desc']})   ").strip()
                if not desc:
                    desc = placeholder['desc']

                price_input = input(f"Ändra pris: ({placeholder['price']})   ").strip()
                if not price_input:
                    price = placeholder['price']
                else:
                    price = float(price_input)
    
                quantity_input = input(f"Ändra antal produkter: ({placeholder['quantity']})   ").strip()
                if not quantity_input:
                    quantity = placeholder['quantity']
                else:
                    quantity = int(quantity_input)

                edit_product(products, id, name, desc, price, quantity)

            if choice == "V":   #visa
                os.system('cls' if os.name == 'nt' else 'clear')

                if 1 <= index <= len(products):
                    selected_product = products[index - 1]
                    id = selected_product['id']
                    print(view_product(products, id))
                    done = input()

                else:
                    print("Ogiltig produkt")
                    sleep(1)

            elif choice == "T":
                os.system('cls' if os.name == 'nt' else 'clear')

                if 1 <= index <= len(products):
                    selected_product = products[index - 1]
                    id = selected_product['id']

                    print(remove_product(products, id))
                    sleep(1)

                else:
                    print("Ogiltig produkt")
                    sleep(1)
        
    except ValueError:
        print("Välj en produkt med siffor")
        sleep(1)