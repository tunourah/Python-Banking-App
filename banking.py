import csv

class Customer:
    def __init__(self, account_id, first_name, last_name, password, checking=0, savings=0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = int(checking)
        self.savings = int(savings)

    @staticmethod
    def generate_account_id():
   
        try:
            with open("bank.csv", "r") as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)   
                rows = [row for row in reader if row]   

            if rows:
                last_account_id = int(rows[-1][0])  
            else:
                last_account_id = 10000   

        except FileNotFoundError:
            last_account_id = 10000  

        return last_account_id + 1  

    @staticmethod
    def add_new_account():
       
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        password = input("Enter your password: ")

       
        account_id = Customer.generate_account_id()
        customer = Customer(account_id, first_name, last_name, password)

      
        with open("bank.csv", "a", newline="") as file:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings"]
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")

            
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                "account_id": customer.account_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "password": customer.password,
                "balance_checking": customer.checking,
                "balance_savings": customer.savings
            })

        print(f"\n✅ Account created successfully! Your account ID is {customer.account_id}")
        print("🔐 Please log in to access banking services.\n")

    @staticmethod
    def login():
       
        while True:
            account_id = input("Enter your Account ID: ")
            password = input("Enter your Password: ")

            try:
                with open("bank.csv", "r") as file:
                    reader = csv.DictReader(file, delimiter=";")
                    for row in reader:
                        if row["account_id"] == account_id and row["password"] == password:
                            print(f"\n✅ Welcome back, {row['first_name']} {row['last_name']}!\n")
                            return Customer(
                                row["account_id"],
                                row["first_name"],
                                row["last_name"],
                                row["password"],
                                row["balance_checking"],
                                row["balance_savings"]
                            )  # Return Customer instance

            except FileNotFoundError:
                print("❌ Error: No accounts found.")
                return None

            error = input("❌ Invalid credentials. Press 1 to try again or any other key to exit: ")
            if error != "1":
                print("👋 Exiting login.")
                return None

class AccountService:
    
    @staticmethod
    def withdraw_from_savings(customer):
        try:
            amount = float(input("Enter amount to withdraw from Savings: "))
        except ValueError:
            print("❌ Invalid amount.")
            return
        if amount > customer.savings:
            print("❌ Insufficient funds in savings.")
        else:
            customer.savings -= amount
            print(f"✅ Withdrawal successful! New savings balance: {customer.savings}")
            AccountService.update_customer_balance(customer)

    @staticmethod
    def withdraw_from_checking(customer):
        try:
            amount = float(input("Enter amount to withdraw from Checking: "))
        except ValueError:
            print("❌ Invalid amount.")
            return
        if amount > customer.checking:
            print("❌ Insufficient funds in checking.")
        else:
            customer.checking -= amount
            print(f"✅ Withdrawal successful! New checking balance: {customer.checking}")
            AccountService.update_customer_balance(customer)

    @staticmethod
    def update_customer_balance(customer, filename="bank.csv"):
        
        updated_rows = []
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file, delimiter=";")
                fieldnames = reader.fieldnames
                for row in reader:
                    if row["account_id"] == str(customer.account_id):
                        row["balance_checking"] = str(customer.checking)
                        row["balance_savings"] = str(customer.savings)
                    updated_rows.append(row)
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(updated_rows)
        except FileNotFoundError:
            print("❌ Error: Bank file not found.")
class BankingSystem:
    
    
    @staticmethod
    def show_services(customer):
        
        while True:
            print("\n" + "=" * 40)
            print("      ✨  AVAILABLE BANKING SERVICES  ✨      ")
            print("=" * 40)
            print("\n ❖ Choose a Service: ")
            print("1️⃣ Withdraw from Savings")
            print("2️⃣ Withdraw from Checking")
            print("3️⃣ Deposit into Savings")
            print("4️⃣ Deposit into Checking")
            print("5️⃣ Transfer from Savings to Checking")
            print("6️⃣ Transfer from Checking to Savings")
            print("7️⃣ Transfer to Another Customer")
            print("8️⃣ Logout")

            choice = input("\n🔹 Enter your choice: ")

            if choice == "1":
                AccountService.withdraw_from_savings(customer)
            elif choice == "2":
                AccountService.withdraw_from_checking(customer)
            elif choice == "3":
                print("💰 Deposit into Savings (Coming Soon)")
            elif choice == "4":
                print("💰 Deposit into Checking (Coming Soon)")
            elif choice == "5":
                print("🔄 Transfer from Savings to Checking (Coming Soon)")
            elif choice == "6":
                print("🔄 Transfer from Checking to Savings (Coming Soon)")
            elif choice == "7":
                print("🔄 Transfer to Another Customer (Coming Soon)")
            elif choice == "8":
                print("\n👋 Logging out. Returning to the main menu.")
                break  
            else:
                print("❌ Invalid choice. Please enter a number from 1 to 8.")

    @staticmethod
    def main():
        
        while True:
            print("\n" + "=" * 40)
            print("      ✨   WELCOME TO NORA BANK   ✨      ")
            print("=" * 40)
            print("\n ❖ Banking Services Available: ")
            print("1️⃣ Create New Account")
            print("2️⃣ Login to Existing Account")
            print("3️⃣ Exit")

            choice = input("\n🔹 Enter your choice: ")

            if choice == "1":
                Customer.add_new_account()
            elif choice == "2":
                customer = Customer.login()
                if customer:
                    BankingSystem.show_services(customer)  
            elif choice == "3":
                print("\n👋 Thank you for using Nora Bank. Goodbye!")
                break  
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")


 
if __name__ == "__main__":
    BankingSystem.main()

# page for the manger and page for coustomer 

# START

# DISPLAY "Welcome to the Banking System"
# DISPLAY "1. Login"
# DISPLAY "2. Create New Account"

# GET user_choice

# IF user_choice == 2 THEN
#     DISPLAY "Enter First Name:"
#     GET first_name
#     DISPLAY "Enter Last Name:"
#     GET last_name
#     DISPLAY "Create a Password:"
#     GET password
#     GENERATE random_account_id
#     CREATE new customer with (first_name, last_name, password, account_id)
#     INITIALIZE checking_account with balance = 0
#     INITIALIZE savings_account with balance = 0
#     STORE customer in database (CSV file)
#     DISPLAY "Account created successfully! Your Account ID is: account_id"

# ELSE IF user_choice == 1 THEN
#     DISPLAY "Enter Account ID:"
#     GET account_id
#     DISPLAY "Enter Password:"
#     GET password
    
#     IF account_id and password match in database THEN
#         DISPLAY "Login Successful!"
        
#         WHILE user is logged in:
#             DISPLAY "1. Deposit Money"
#             DISPLAY "2. Withdraw Money"
#             DISPLAY "3. Transfer Money"
#             DISPLAY "4. View Transactions"
#             DISPLAY "5. Logout"
            
#             GET action_choice
            
#             IF action_choice == 1 THEN
#                 DISPLAY "Choose Account: 1. Checking  2. Savings"
#                 GET account_type
#                 DISPLAY "Enter Amount to Deposit:"
#                 GET deposit_amount
#                 ADD deposit_amount to chosen account balance
#                 LOG transaction
                
#             ELSE IF action_choice == 2 THEN
#                 DISPLAY "Choose Account: 1. Checking  2. Savings"
#                 GET account_type
#                 DISPLAY "Enter Amount to Withdraw:"
#                 GET withdraw_amount
#                 IF balance is sufficient THEN
#                     SUBTRACT withdraw_amount from chosen account balance
#                     LOG transaction
#                 ELSE IF balance is insufficient THEN
#                     APPLY overdraft protection rules
#                     LOG overdraft fee
                
#             ELSE IF action_choice == 3 THEN
#                 DISPLAY "Choose Account to Transfer FROM: 1. Checking  2. Savings"
#                 GET from_account
#                 DISPLAY "Choose Account to Transfer TO: 1. Checking  2. Savings OR Another Customer"
#                 GET to_account
#                 DISPLAY "Enter Amount to Transfer:"
#                 GET transfer_amount
#                 CHECK if sufficient balance
#                 TRANSFER money
#                 LOG transaction
                
#             ELSE IF action_choice == 4 THEN
#                 DISPLAY transaction history
                
#             ELSE IF action_choice == 5 THEN
#                 DISPLAY "Logging Out..."
#                 BREAK LOOP
                
#         END WHILE
        
#     ELSE
#         DISPLAY "Invalid Login Credentials"

# END
