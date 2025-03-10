import csv

class Customer:
  
    
    def __init__(self, account_id, first_name, last_name, password, balance_checking=0.0, balance_savings=0.0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = float(balance_checking)
        self.balance_savings = float(balance_savings)

    def save_to_file(self, filename='bank.csv'):
        """Saves customer information to a CSV file."""
        with open(filename, 'a', newline='') as csv_file:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')

            if csv_file.tell() == 0:  
                csv_writer.writeheader()

            csv_writer.writerow({
                "account_id": self.account_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password": self.password,
                "balance_checking": self.balance_checking,
                "balance_savings": self.balance_savings
            })

class Bank:
    
    
    @staticmethod
    def is_account_id_unique(account_id, filename='bank.csv'):
       
        try:
            with open(filename, 'r', newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                for row in csv_reader:
                    if row["account_id"] == str(account_id):
                        return False
        except FileNotFoundError:
            return True  
        return True  

    @staticmethod
    def login_customer(account_id, password, filename='bank.csv'):
       
        try:
            with open(filename, 'r', newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                for row in csv_reader:
                    if row["account_id"] == account_id and row["password"] == password:
                        print(f"\n✅ Welcome back, {row['first_name']} {row['last_name']}!\n")
                        return Customer(row["account_id"], row["first_name"], row["last_name"], row["password"], row["balance_checking"], row["balance_savings"])
        except FileNotFoundError:
            print("❌ No accounts found.")
        return None

    

    @staticmethod
    def create_customer():
        
        print("\n📄 Enter New Customer Details:")
        
        while True:
            try:
                account_id = input("Enter Account ID: ")
                if Bank.is_account_id_unique(account_id):
                    break
                else:
                    print("❌ Account ID already exists. Try another one.")
            except ValueError:
                print("❌ Please enter a valid numeric account ID.")

        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        password = input("Enter Password: ")
        
        while True:
            try:
                balance_checking = float(input("Enter Checking Account Balance: "))
                balance_savings = float(input("Enter Savings Account Balance: "))
                break
            except ValueError:
                print("❌ Please enter a valid number for balance.")

        new_customer = Customer(account_id, first_name, last_name, password, balance_checking, balance_savings)
        new_customer.save_to_file()
        print(f"✅ Account created successfully for {first_name} {last_name}!\n")
        BankingSystem.banking_menu(new_customer)

    @staticmethod
    def banking_menu(customer):
        
        while True:
            print("\n🏦 Banking Options:")
            print("1️⃣ Withdraw Money")
            print("2️⃣ Deposit Money")
            print("3️⃣ Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                Transaction.withdraw_money(customer)
            elif choice == "2":
                Transaction.deposit_money(customer)
            elif choice == "3":
                print("👋 Thank you for using Nora Bank. Goodbye!")
                break
            else:
                print("❌ Invalid option. Please select again.")

    @staticmethod
    def login():
      
        account_id = input("Enter your Account ID: ")
        password = input("Enter your Password: ")
        customer = Bank.login_customer(account_id, password)

        if customer:
            BankingSystem.banking_menu(customer)
        else:
            print("❌ Login failed. Try again.")

    @staticmethod
    def main():
       
        print("\n💳 Welcome to Nora Bank!\n")
        print("1️⃣ Create New Account")
        print("2️⃣ Login to Existing Account")
        
        while True:
            option = input("Enter your choice: ")
            if option == "1":
                BankingSystem.create_customer()
                break
            elif option == "2":
                BankingSystem.login()
                break
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    BankingSystem.main()
