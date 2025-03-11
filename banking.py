import csv

class Customer:
    def __init__(self, account_id, first_name, last_name, password, checking=0, savings=0, overdraft_count=0, status="active"):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = int(float(checking))
        self.savings = int(float(savings))
        self.overdraft_count = int(overdraft_count)
        self.status = status   

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
        
        customer = Customer(account_id, first_name, last_name, password, 0, 0, 0, "active")

        with open("bank.csv", "a", newline="") as file:
            fieldnames = ["account_id", "first_name", "last_name", "password",
                          "balance_checking", "balance_savings", "overdraft_count", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({
                "account_id": customer.account_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "password": customer.password,
                "balance_checking": customer.checking,
                "balance_savings": customer.savings,
                "overdraft_count": customer.overdraft_count,
                "status": customer.status
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
                                row["balance_savings"],
                                row.get("overdraft_count", 0),
                                row.get("status", "active")
                            )
            except FileNotFoundError:
                print("❌ Error: No accounts found.")
                return None

            error = input("❌ Invalid credentials. Press 1 to try again or any other key to exit: ")
            if error != "1":
                print("👋 Exiting login.")
                return None


class AccountService:
   
    
    @staticmethod
    def update_customer_balance(customer, filename="bank.csv"):
        
        expected_fieldnames = [
            "account_id", "first_name", "last_name", "password",
            "balance_checking", "balance_savings", "overdraft_count", "status"
        ]
        updated_rows = []
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file, delimiter=";")
                fieldnames = reader.fieldnames if reader.fieldnames is not None else expected_fieldnames
                 
                for key in expected_fieldnames:
                    if key not in fieldnames:
                        fieldnames.append(key)
                for row in reader:
                    for key in expected_fieldnames:
                        if key not in row:
                            if key == "overdraft_count":
                                row[key] = "0"
                            elif key == "status":
                                row[key] = "active"
                            else:
                                row[key] = ""
                    if row["account_id"] == str(customer.account_id):
                        row["balance_checking"] = str(customer.checking)
                        row["balance_savings"] = str(customer.savings)
                        row["overdraft_count"] = str(customer.overdraft_count)
                        row["status"] = customer.status
                    updated_rows.append(row)
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=expected_fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(updated_rows)
        except FileNotFoundError:
            print("❌ Error: Bank file not found.")

    @staticmethod
    def withdraw_from_account(customer, account_type):
        
        if customer.status != "active":
            print("❌ Your account is deactivated due to multiple overdrafts. Please deposit funds to reactivate.")
            return

        if account_type.lower() == "checking":
            balance = customer.checking
        elif account_type.lower() == "savings":
            balance = customer.savings
        else:
            print("❌ Invalid account type.")
            return

        try:
            amount = float(input(f"Enter amount to withdraw from {account_type.capitalize()}: "))
        except ValueError:
            print("❌ Invalid amount.")
            return

        fee = 35.0   

        
        if balance < 0:
            if amount > 100:
                print("❌ Cannot withdraw more than $100 when the account is negative.")
                return
            new_balance = balance - amount - fee
            if new_balance < -100:
                print("❌ Withdrawal would exceed the overdraft limit of -$100.")
                return
            customer.overdraft_count += 1
            print(f"✅ Withdrawal successful! {account_type.capitalize()} balance: {balance} -> {new_balance} (including ${fee} overdraft fee)")
        else:
          
            if balance - amount < 0:
                new_balance = balance - amount - fee
                if new_balance < -100:
                    print("❌ Withdrawal would exceed the overdraft limit of -$100.")
                    return
                customer.overdraft_count += 1
                print(f"✅ Withdrawal successful! {account_type.capitalize()} balance: {balance} -> {new_balance} (including ${fee} overdraft fee)")
            else:
                
                new_balance = balance - amount
                print(f"✅ Withdrawal successful! {account_type.capitalize()} balance: {balance} -> {new_balance}")

         
        if account_type.lower() == "checking":
            customer.checking = new_balance
        else:
            customer.savings = new_balance

        
        if customer.overdraft_count >= 2:
            customer.status = "deactivated"
            print("❌ Your account has been deactivated due to multiple overdrafts.")

        AccountService.update_customer_balance(customer)

    @staticmethod
    def deposit_to_account(customer, account_type):
        
        try:
            amount = float(input(f"Enter amount to deposit into {account_type.capitalize()}: "))
        except ValueError:
            print("❌ Invalid amount.")
            return

        if account_type.lower() == "checking":
            old_balance = customer.checking
            new_balance = old_balance + amount
            customer.checking = new_balance
        elif account_type.lower() == "savings":
            old_balance = customer.savings
            new_balance = old_balance + amount
            customer.savings = new_balance
        else:
            print("❌ Invalid account type.")
            return

        print(f"✅ Deposit successful! {account_type.capitalize()} balance is now {new_balance}.")

       
        if new_balance >= 0 and customer.status == "deactivated":
            print("💡 Account reactivated after deposit. Overdraft fees and count reset.")
            customer.overdraft_count = 0
            customer.status = "active"

        AccountService.update_customer_balance(customer)


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
            print("5️⃣ Transfer from Savings to Checking (Coming Soon)")
            print("6️⃣ Transfer from Checking to Savings (Coming Soon)")
            print("7️⃣ Transfer to Another Customer (Coming Soon)")
            print("8️⃣ Logout")

            choice = input("\n🔹 Enter your choice: ")

            if choice == "1":
                AccountService.withdraw_from_account(customer, "savings")
            elif choice == "2":
                AccountService.withdraw_from_account(customer, "checking")
            elif choice == "3":
                AccountService.deposit_to_account(customer, "savings")
            elif choice == "4":
                AccountService.deposit_to_account(customer, "checking")
            elif choice in ("5", "6", "7"):
                print("🔄 Feature coming soon!")
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
