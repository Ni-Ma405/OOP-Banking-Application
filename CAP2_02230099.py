#FCollowing packages are imported to be used in the code below
import os
import random
import string

#  BSNK_DATA_FILE is declared to store account details
BANK_DATA_FILE = "bank_accounts.txt"

#  To represent an individual bank account the BankAccount class was defined
class BankAccount:
    #Using constructor, foollowing properties passed in the parameter was initialized
    def __init__(self, acc_num, acc_pass, acc_type, acc_bal=0):
        self.acc_num = acc_num  # For account number 
        self.acc_pass = acc_pass # For account password 
        self.acc_type = acc_type #  Account type with the provided value
        self.acc_balance = acc_bal # It will store account balance. default value is zero

    # this block of codes is a method for depositing  money into the account
    def deposit(self, amount):
        self.acc_bal += amount 
        print(f"Deposited {amount}. New balance: {self.acc_bal}")# it will display the deposit amount and new balance 

    # this sets of codes is for withdrawing money from the account
    def withdraw(self, amount):
        if amount <= self.acc_bal: # it determines if the account has sufficient balance to withdraw
            self.acc_bal -= amount # Deduct the amount from the current balance
            print(f"Withdrew {amount}. New balance: {self.acc_bal}")# it prints the amount withdrawn and the new balance
        else:
            print("Insufficient funds.") # it prints an error message if balance is not sufficient

    # It converts account details to string for file storage
    # In this code a single string is created  that contains all the essential details of the account
    def to_string(self):
        return f"{self.acc_num},{self.acc_pass},{self.acc_type},{self.acc_bal}\n"

# BankSystem class is defined to manage multiple accounts
class BankSystem:
    def __init__(self):
        self.bank_accounts = self.load_accounts() # Load existing accounts from file

    # This block of code will get through the file and store bank information in the nested dictionarye
    def load_accounts(self):
        accounts = {}
        if os.path.exists(BANK_DATA_FILE): # it checks if the file exists or not
            with open(BANK_DATA_FILE, "r") as file:
                for line in file:
                    acc_num, acc_pass, acc_type, acc_bal = line.strip().split(",")
                    accounts[acc_num] = BankAccount(acc_num, acc_pass, acc_type, float(acc_bal))# Create BankAccount object and add to dictionary
        return accounts

    # For this, bank accounts are saved in the accounts.txt  file
    def save_accounts(self):
        with open(BANK_DATA_FILE, "w") as file: #File is been opened
            for account in self.bank_accounts.values(): # Then iteration is done through all accounts
                file.write(account.to_string())# Writes each account to the file

    # For the new users, new bank account should be created. Therefore this block of code creates a new account with a unique number and password
    def create_account(self, acc_type):
        acc_num = ''.join(random.choices(string.digits, k=10))# For Generating a random 10-digit account number
        acc_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=8))# For generating a random 8-character password
        self.bank_accounts[acc_num] = BankAccount(acc_num, acc_pass, acc_type)
        print(f"Account created. Number: {acc_num}, Password: {acc_pass}") # Display account details to user

    # Login section where user can login to their accountn
    def login(self, acc_num, acc_pass):
        account = self.bank_accounts.get(acc_num)  # Retrieve account using account number
        if account and account.acc_pass == acc_pass:# It will check if account exists and password matches
            print(f"Login successful. Welcome {account.acc_type} Account holder.")# If so, success message is been displayed
            return account 
        print("Invalid account number or password.")# If login credential does not match, error message is displayed
        return None # Return None if login fails


    # For transfering money from one account to another
    def transfer_money(self, from_account, to_acc_num, amount):
        to_account = self.bank_accounts.get(to_acc_num)# Retrieve the destination account
        if to_account and from_account.acc_balance >= amount:# Check if destination account exists and sufficient funds are available
            from_account.withdraw(amount) # For withdrawing amount from the source account
            to_account.deposit(amount) # For depositing amount into the destination account
            self.save_accounts() # Save updated accounts to file
            print(f"Transferred {amount} to {to_acc_num}.") # Success message if transcation was successful
        else:
            print("Transfer failed. Check accounts and balance.") # If failed, error message will be displayed

# Main function to run the banking application
def main():
    bank_system = BankSystem() # Create an instance of BankSystem
    while True:
        print("\n1. Open a new account\n2. Login\n3. Exit") # Display main menu options for user to choose
        choice = input("Enter choice: ") # user will give input here
        #Base on the user in put, following code will run
        if choice == "1": #This choice is for creating new account
            acc_type = input("Enter account type (Personal/Business): ") # Get input from user the type of account they want to create
            bank_system.create_account(acc_type) # Create new account
        elif choice == "2":#This choice is for loginn section
            acc_num = input("Account number: ")# Get account number from user
            acc_pass = input("Password: ")# Get password from user

            account = bank_system.login(acc_num, acc_pass)# Attempt to login
            if account:
                while True: #If login is successful
                    print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Logout") #Following option are displayed
                    action = input("Enter action: ")
                    if action == "1":
                        print(f"Balance: {account.acc_bal}") # Display balance
                    elif action == "2":
                        amount = float(input("Amount to deposit: ")) # Get deposit amount
                        account.deposit(amount) # Deposit amount into account
                        bank_system.save_accounts() # Save updated accounts to file
                    elif action == "3":
                        amount = float(input("Amount to withdraw: "))# Get withdrawal amount
                        account.withdraw(amount) # Withdraw amount from account
                        bank_system.save_accounts() # Save updated accounts to file
                    elif action == "4":
                        to_acc_num = input("To account number: ") # Get destination account number
                        amount = float(input("Amount to transfer: ")) # Get transfer amount
                        bank_system.transfer_money(account, to_acc_num, amount) # Transfer money
                    elif action == "5":
                        break # It will Logout
                    else:
                        print("Invalid action.") # Error message for invalid action
        elif choice == "3":
            break # Exit the application
        else:
            print("Invalid choice.")  # Error message for invalid choice

if __name__ == "__main__":
    main() # main function called to Run the program
 