import csv
import datetime
import os

class Customer:
    def __init__(self, account_id, first_name, last_name, password, checking=0, savings=0, overdraft_count=0, status="active"):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = float(checking)
        self.savings = float(savings)
        self.overdraft_count = int(overdraft_count)
        self.status = status  

    @staticmethod
    def generate_account_id():
        try:
            with open("bank.csv", "r") as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)  # Skip header
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
                        if row["account_id"] == str(account_id) and row["password"] == password:
                            print(f"\n✅ Welcome back, {row['first_name']} {row['last_name']}!\n")
                            return Customer(
                                str(row["account_id"]),  # Ensure account_id is a string
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

class TransactionService:
    
    
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
                # Ensure expected keys are in the header
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
        # If already negative or withdrawal makes balance negative:
        if balance < 0 or (balance - amount < 0):
            new_balance = balance - amount - fee
            if new_balance < -100:
                print("❌ Withdrawal would exceed the overdraft limit of -$100.")
                return
            # When account is already negative, limit the withdrawal to $100 maximum.
            if balance < 0 and amount > 100:
                print("❌ Cannot withdraw more than $100 when the account is negative.")
                return
            customer.overdraft_count += 1
            print(f"✅ Withdrawal successful! {account_type.capitalize()} balance: {balance} -> {new_balance} (including ${fee} fee)")
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

        TransactionService.update_customer_balance(customer)

    @staticmethod
    def deposit_to_account(customer, account_type):
        try:
            amount = float(input(f"Enter amount to deposit into {account_type.capitalize()}: "))
        except ValueError:
            print("❌ Invalid amount.")
            return

        if account_type.lower() == "checking":
            customer.checking += amount
            new_balance = customer.checking
        elif account_type.lower() == "savings":
            customer.savings += amount
            new_balance = customer.savings
        else:
            print("❌ Invalid account type.")
            return

        print(f"✅ Deposit successful! {account_type.capitalize()} balance is now {new_balance}.")

        if new_balance >= 0 and customer.status == "deactivated":
            print("💡 Account reactivated after deposit. Overdraft count reset.")
            customer.overdraft_count = 0
            customer.status = "active"

        TransactionService.update_customer_balance(customer)


class TransferService:
    
    
    @staticmethod
    def transfer_from_savings_to_checking(customer):
        try:
            amount = float(input("Enter amount to transfer from Savings to Checking: "))
        except ValueError:
            print("❌ Invalid amount.")
            return
        fee = 35.0
        current_balance = customer.savings

        if current_balance >= amount:
            # Simple transfer
            customer.savings = current_balance - amount
            customer.checking += amount
            print(f"✅ Transfer successful! Savings: {current_balance} -> {customer.savings}, Checking increased by {amount}")
        else:
            # Overdraft occurs
            new_balance = current_balance - amount - fee
            if new_balance < -100:
                print("❌ Transfer would exceed the overdraft limit of -$100.")
                return
            customer.savings = new_balance
            customer.checking += amount
            customer.overdraft_count += 1
            print(f"✅ Transfer successful! Savings: {current_balance} -> {new_balance} (including ${fee} fee), Checking increased by {amount}")

        if customer.overdraft_count >= 2:
            customer.status = "deactivated"
            print("❌ Your account has been deactivated due to multiple overdrafts.")

        TransactionService.update_customer_balance(customer)

    @staticmethod
    def transfer_from_checking_to_savings(customer):
        try:
            amount = float(input("Enter amount to transfer from Checking to Savings: "))
        except ValueError:
            print("❌ Invalid amount.")
            return
        fee = 35.0
        current_balance = customer.checking

        if current_balance >= amount:
            customer.checking = current_balance - amount
            customer.savings += amount
            print(f"✅ Transfer successful! Checking: {current_balance} -> {customer.checking}, Savings increased by {amount}")
        else:
            new_balance = current_balance - amount - fee
            if new_balance < -100:
                print("❌ Transfer would exceed the overdraft limit of -$100.")
                return
            customer.checking = new_balance
            customer.savings += amount
            customer.overdraft_count += 1
            print(f"✅ Transfer successful! Checking: {current_balance} -> {new_balance} (including ${fee} fee), Savings increased by {amount}")

        if customer.overdraft_count >= 2:
            customer.status = "deactivated"
            print("❌ Your account has been deactivated due to multiple overdrafts.")

        TransactionService.update_customer_balance(customer)

    @staticmethod
    def transfer_to_another_customer(customer):
        target_account_id = input("Enter the target customer's Account ID: ")
        try:
            amount = float(input("Enter amount to transfer: "))
        except ValueError:
            print("❌ Invalid amount.")
            return
        source_choice = input("Transfer from which account? (Enter 'checking' or 'savings'): ").strip().lower()
        if source_choice not in ("checking", "savings"):
            print("❌ Invalid account type.")
            return

        fee = 35.0
        source_balance = customer.checking if source_choice == "checking" else customer.savings

        if source_balance >= amount:
            new_source_balance = source_balance - amount
            print("✅ Transfer initiated without overdraft fee.")
        else:
            new_source_balance = source_balance - amount - fee
            if new_source_balance < -100:
                print("❌ Transfer would exceed the overdraft limit of -$100.")
                return
            customer.overdraft_count += 1
            print(f"✅ Transfer initiated with overdraft fee. Fee of ${fee} applied.")

        if source_choice == "checking":
            customer.checking = new_source_balance
        else:
            customer.savings = new_source_balance

       
        target_found = False
        updated_rows = []
        filename = "bank.csv"
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file, delimiter=";")
                fieldnames = reader.fieldnames
                for row in reader:
                    if row["account_id"] == target_account_id:
                        target_checking = float(row["balance_checking"])
                        new_target_balance = target_checking + amount
                        row["balance_checking"] = str(new_target_balance)
                        target_found = True
                    updated_rows.append(row)
            if not target_found:
                print("❌ Target account not found.")
                return
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(updated_rows)
            print(f"✅ Transfer of ${amount} to account {target_account_id} successful!")
        except FileNotFoundError:
            print("❌ Error: Bank file not found.")
            return

        if customer.overdraft_count >= 2:
            customer.status = "deactivated"
            print("❌ Your account has been deactivated due to multiple overdrafts.")

        TransactionService.update_customer_balance(customer)


class TransactionHistory:
    FILE_NAME = "transaction_history.csv"

    @staticmethod
    def log_transaction(account_id, transaction_type, amount, resulting_balance):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      
        file_exists = os.path.isfile(TransactionHistory.FILE_NAME)

        with open(TransactionHistory.FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)

           
            if not file_exists:
                writer.writerow(["account_id", "timestamp", "transaction_type", "amount", "resulting_balance"])
 
            writer.writerow([str(account_id), timestamp, transaction_type, amount, resulting_balance])

    @staticmethod
    def view_transactions(account_id):
        print("\n📜 Transaction History:")
        print("=" * 50)
        try:
            with open(TransactionHistory.FILE_NAME, mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                
                transactions = [row for row in reader if row[0].strip() == str(account_id).strip()]

                if not transactions:
                    print("No transaction history found.")
                    return
                
                print(f"{'Date & Time':<20} {'Type':<15} {'Amount':<10} {'Balance':<10}")
                print("-" * 50)
                for row in transactions:
                    print(f"{row[1]:<20} {row[2]:<15} {row[3]:<10} {row[4]:<10}")
        except FileNotFoundError:
            print("No transaction history available yet.")

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
            print("8️⃣ View Transaction History (Cooming Soon)")
            print("9️⃣ Logout")

            choice = input("\n🔹 Enter your choice: ")

            if choice == "1":
                TransactionService.withdraw_from_account(customer, "savings")
            elif choice == "2":
                TransactionService.withdraw_from_account(customer, "checking")
            elif choice == "3":
                TransactionService.deposit_to_account(customer, "savings")
            elif choice == "4":
                TransactionService.deposit_to_account(customer, "checking")
            elif choice == "5":
                TransferService.transfer_from_savings_to_checking(customer)
            elif choice == "6":
                TransferService.transfer_from_checking_to_savings(customer)
            elif choice == "7":
                TransferService.transfer_to_another_customer(customer)
            elif choice == "8":
                TransactionHistory.view_transactions(customer.account_id)
            elif choice == "9":
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
