import csv

   

import csv

class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking, balance_savings):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = balance_checking
        self.balance_savings = balance_savings

    def add_new_customer(self):
        with open('bank.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow([
                self.account_id,
                self.first_name,
                self.last_name,
                self.password,
                self.balance_checking,
                self.balance_savings
            ])

 
def create_customer():
    print("\nEnter New Customer Details:")

    account_id = int(input("Enter Account ID: "))
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    password = input("Enter Password: ")
    balance_checking = float(input("Enter Checking Account Balance: "))
    balance_savings = float(input("Enter Savings Account Balance: "))

 
    new_customer = Customer(account_id, first_name, last_name, password, balance_checking, balance_savings)
    
 
    new_customer.add_new_customer()
    print("✅ Customer added successfully!\n")

 
create_customer()