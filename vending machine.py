import random

coins = 100  # Money available to spend

vending_items = {  # Stores items with name, price, and stock
        1: {"name": "Cola", "price": 20, "stock": 5},
        2: {"name": "Water", "price": 15, "stock": 5},
        3: {"name": "Biscuit", "price": 25, "stock": 5},
        4: {"name": "Sandwich", "price": 40, "stock": 5}
    }

item_suggestions = {  # Stores suggested pairs for each item
    1: {"suggestion": "Sandwich", "id": 4},
    2: {"suggestion": "Biscuit", "id": 3},
    3: {"suggestion": "Water", "id": 2},
    4: {"suggestion": "Cola", "id": 1}
}

def start_game():
    print(f'You currently have {coins} AED')
    user_consent = input("Would you like to earn more money? (yes/no): ").lower().strip()
    if user_consent == "yes":
        earn_coins()
    else:
        vending_machine()

def earn_coins():
    global coins
    random_number = random.randint(1, 10)  # Generate random number between 1 and 10
    print("Welcome to the number guessing game!")
    toggle = True
    while toggle:
        try:
            user_guess = int(input("Enter a number: "))
            if user_guess != random_number:
                print("Try again!")
                continue
            coins += 10  # Add 10 coins if guess is correct
            print(f'You now have {coins} coins')
                
            continue_game = input("Do you want to play again? (yes/no): ").lower().strip()
            if continue_game == "no":
                toggle = False
                vending_machine()
        except ValueError:
            print("Enter a valid number!")

def display_items():
    print("Vending Machine")
    for key, item in vending_items.items():  # Loop through all items
        stock_status = f"(Stock: {item['stock']})" if item['stock'] > 0 else "(OUT OF STOCK)"
        print(f"{key}. {item['name']} - {item['price']} AED {stock_status}")

def check_all_out_of_stock():
    for item in vending_items.values():  # Check each item's stock
        if item['stock'] > 0:
            return False
    return True  # All items are out of stock

def suggest_item(purchased_item_id):
    global coins
    
    suggestion = item_suggestions[purchased_item_id]  # Get the suggested pairing
    suggested_item = vending_items[suggestion["id"]]
    
    if suggested_item['stock'] == 0:  # Check if suggested item is in stock
        print(f"\nWe would suggest {suggestion['suggestion']}, but it's currently out of stock!")
        return True
    
    print(f"\nHow about pairing it with a {suggestion['suggestion']}? ({suggested_item['price']} AED) - Stock: {suggested_item['stock']}")
    response = input("Would you like to buy it? (yes/no): ").lower().strip()
    
    if response == "yes":
        while True:
            money = int(input(f"Insert money for {suggested_item['name']} ({suggested_item['price']} AED):"))
            
            if money > coins:  # Check if user has enough coins
                print(f"You only have {coins} coins to input!")
                continue
            
            if money < suggested_item["price"]:  # Check if money inserted is enough
                earn_money = input("Not enough money! Would you like to earn more money? (yes/no):").lower().strip()
                if earn_money == "yes":
                    earn_coins()
                    return True
                else:
                    print("See you soon!")
                    return False
            
            change = money - suggested_item["price"]  # Calculate change
            coins -= suggested_item["price"]  # Deduct price from coins
            suggested_item['stock'] -= 1  # Decrease stock by 1
            print(f"Here is your {suggested_item['name']}. Your change is: {change} \nYou now have {coins} coins.")
            
            if suggested_item['stock'] == 0:  # Check if item is now out of stock
                print(f"WARNING: {suggested_item['name']} is now out of stock!")
            
            return True
    
    return True

def buy_items():
    global coins
    
    if check_all_out_of_stock():  # Check if all items are out of stock
        print("\nWARNING: Sorry! All items are out of stock. The vending machine is empty!")
        print("Thank you for your patronage!")
        return False
    
    while True:
        try:
            choice = int(input("Select a number (1, 2, 3, 4): "))
            if choice not in vending_items:  # Validate user selection
                print("Invalid selection")
                continue
            
            item = vending_items[choice]
            
            if item['stock'] == 0:  # Check if selected item is in stock
                print(f"Sorry! {item['name']} is out of stock. Please choose another item.")
                continue
            
            while True:
                money = int(input(f"Insert money for {item['name']} ({item['price']} AED):"))
                
                if money > coins:  # Check if user has enough coins
                    print(f"You only have {coins} AED to input!")
                    continue
                
                if money < item["price"]:  # Check if money inserted is enough
                    earn_money = input("Not enough money! Would you like to earn more money? (yes/no):").lower().strip()
                    if earn_money == "yes":
                        earn_coins()
                        return True
                    else:
                        print("See you soon!")
                        return False
                
                change = money - item["price"]  # Calculate change
                coins -= item["price"]  # Deduct price from coins
                item['stock'] -= 1  # Decrease stock by 1
                print(f"Here is your {item['name']}. Your change is: {change} \nYou now have {coins} coins.")
                
                if item['stock'] == 0:  # Check if item is now out of stock
                    print(f"{item['name']} is out of stock!")
                
                result = suggest_item(choice)  # Suggest a pairing item
                if result == False:
                    return False
                
                break
            
            break
            
        except ValueError:
            print("Enter a valid number!")
    
    return True

def vending_machine():
    if check_all_out_of_stock():  # Check if machine is empty before displaying
        print("\nSorry! All items are out of stock. The vending machine is empty!")
        print("Thank you for your patronage!")
        return
    
    print(f'You have {coins} coins')
    display_items()  # Show available items
    result = buy_items()  # Start purchase process
    
    if result == False:  # User chose to exit
        return
    
    again = input("Do you want to buy again? (yes/no): ").lower().strip()
    if again == "yes":
        vending_machine()  # Loop back to vending machine
    else:
        print("Thank you for buying!")

start_game()  # Start the program