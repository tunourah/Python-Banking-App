import csv

class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking, balance_savings):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = balance_checking
        self.balance_savings = balance_savings

    def add_new_customer(self, filename='bank.csv'):
        """Appends a new customer record to the CSV file."""
        with open(filename, 'a', newline='') as csv_file:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')

       
            csv_writer.writerow({
                "account_id": self.account_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password": self.password,
                "balance_checking": self.balance_checking,
                "balance_savings": self.balance_savings
            })

def is_account_id_unique(account_id, filename='bank.csv'):
    """Check if the account ID already exists in the CSV file."""
    try:
        with open(filename, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                if row["account_id"] == str(account_id): 
                    return False  
    except FileNotFoundError:
        return True  
    return True  

 
def create_customer():
    print("\nEnter New Customer Details:")

    while True:
        account_id = int(input("Enter Account ID: "))

 
        if is_account_id_unique(account_id):
            break
        else:
            print("❌ Account ID already exists. Please enter a unique ID.")

    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    password = input("Enter Password: ")
    balance_checking = float(input("Enter Checking Account Balance: "))
    balance_savings = float(input("Enter Savings Account Balance: "))

 
    new_customer = Customer(account_id, first_name, last_name, password, balance_checking, balance_savings)
    
 
    new_customer.add_new_customer()
    print("✅ Customer added successfully!\n")
 
create_customer()
