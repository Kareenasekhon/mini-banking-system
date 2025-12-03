import json
import os
import getpass
from datetime import datetime

# File paths for data storage
USERS_FILE = 'users.json'
TRANSACTIONS_FILE = 'transactions.json'

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    return {}

def save_data(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving {file_path}: {e}")

def create_user():
   
    users = load_data(USERS_FILE)
    
    while True:
        username = input("Enter a new username: ").strip()
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
        if username in users:
            print("Username already exists. Please try again.")
            continue
        break
    
    while True:
        password = getpass.getpass("Enter a new password: ")
        if not password:
            print("Password cannot be empty. Please try again.")
            continue
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue
        break
    
    users[username] = password
    save_data(USERS_FILE, users)
    print("User account created successfully!")
    return username

def login():
    users = load_data(USERS_FILE)
    
    if not users:
        print("No users found. Let's create a new account!")
        return create_user()
    
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        username = input("Enter your username: ").strip()
        if not username:
            print("Username cannot be empty.")
            attempts += 1
            continue
            
        if username not in users:
            print("Username not found.")
            attempts += 1
            continue
            
        password = getpass.getpass("Enter your password: ")
        if users[username] != password:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Incorrect password. {remaining} attempts remaining.")
            else:
                print("Too many failed attempts. Access denied.")
                return None
        else:
            print("Login successful!")
            return username
    
    return None

def initialize_account(username):
   
    transactions = load_data(TRANSACTIONS_FILE)
    if username not in transactions:
        transactions[username] = {
            'balance': 0.0,
            'history': []
        }
        save_data(TRANSACTIONS_FILE, transactions)
        print(f"Account initialized for {username} with starting balance of $0.00")

def deposit(username):
   
    transactions = load_data(TRANSACTIONS_FILE)
    
    while True:
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("Deposit amount must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
    
    transactions[username]['balance'] += amount
    transaction_record = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'Deposit',
        'amount': amount,
        'balance': transactions[username]['balance']
    }
    transactions[username]['history'].append(transaction_record)
    
    save_data(TRANSACTIONS_FILE, transactions)
    print(f"✅ Deposited ${amount:.2f}. New balance: ${transactions[username]['balance']:.2f}")

def withdraw(username):
   
    transactions = load_data(TRANSACTIONS_FILE)
    current_balance = transactions[username]['balance']
    
    if current_balance <= 0:
        print("❌ Insufficient balance. Cannot withdraw from empty account.")
        return
    
    while True:
        try:
            amount = float(input(f"Enter amount to withdraw (Available: ${current_balance:.2f}): $"))
            if amount <= 0:
                print("Withdrawal amount must be positive. Please try again.")
                continue
            if amount > current_balance:
                print(f"❌ Insufficient balance. Available: ${current_balance:.2f}")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
    
    transactions[username]['balance'] -= amount
    transaction_record = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'Withdrawal',
        'amount': amount,
        'balance': transactions[username]['balance']
    }
    transactions[username]['history'].append(transaction_record)
    
    save_data(TRANSACTIONS_FILE, transactions)
    print(f"✅ Withdrew ${amount:.2f}. New balance: ${transactions[username]['balance']:.2f}")

def check_balance(username):
    
    transactions = load_data(TRANSACTIONS_FILE)
    balance = transactions[username]['balance']
    print(f"💰 Current balance: ${balance:.2f}")

def view_transactions(username):
   
    transactions = load_data(TRANSACTIONS_FILE)
    history = transactions[username]['history']
    
    if not history:
        print("📋 No transactions found.")
        return
    
    print(f"\n📋 Transaction History for {username}:")
    print("=" * 70)
    print(f"{'Date':<20} {'Type':<12} {'Amount':<12} {'Balance':<12}")
    print("-" * 70)
    
    for transaction in history:
        print(f"{transaction['date']:<20} {transaction['type']:<12} "
              f"${transaction['amount']:<11.2f} ${transaction['balance']:<11.2f}")
    print("=" * 70)

def main_menu(username):
    
    while True:
        print(f"\n🏦 Welcome to Mini Banking System - {username}")
        print("=" * 50)
        print("1. 💰 Deposit Money")
        print("2. 💸 Withdraw Money")
        print("3. 💳 Check Balance")
        print("4. 📋 View Transaction History")
        print("5. 🚪 Exit")
        print("=" * 50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            deposit(username)
        elif choice == '2':
            withdraw(username)
        elif choice == '3':
            check_balance(username)
        elif choice == '4':
            view_transactions(username)
        elif choice == '5':
            print("👋 Thank you for using Mini Banking System. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please enter a number between 1-5.")


def main():
    print("🏦 Welcome to Mini Banking Simulation System!")
    print("=" * 50)

    print("1. Login")
    print("2. Create New Account")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        username = login()
    elif choice == "2":
        username = create_user()
    else:
        print("❌ Invalid choice. Exiting.")
        return

    if username:
        initialize_account(username)
        main_menu(username)
    else:
        print("❌ Authentication failed. Exiting.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try running the program again.")
