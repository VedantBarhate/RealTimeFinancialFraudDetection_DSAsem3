from account import AccountWrapper
from transaction import TransactionWrapper
from graph import GraphWrapper
from bst import BSTWrapper
from datetime import datetime

from acting_db import Acting_DB

class AppInterface:
    def __init__(self, db : Acting_DB):
        self.db = db
        self.accounts = None
        self.nodes = None
        self.graph : GraphWrapper = None
        self.bst : BSTWrapper = None
        self.__load_data_from_db()

    def __load_data_from_db(self):
        self.accounts = self.db.accounts
        self.nodes = self.db.nodes
        self.graph = self.db.graph
        self.bst = self.db.bst

    def create_account(self):
        acc_num = int(input("Enter New Account number: "))
        if acc_num in self.accounts:
            print("Account already exists!")
            return
        account = AccountWrapper(acc_num)
        self.accounts[acc_num] = account
        node = self.graph.add_node(account)
        self.nodes[acc_num] = node
        self.bst.insert(account)

    def create_transaction(self):
        sender = int(input("Enter Sender Account Number: "))
        receiver = int(input("Enter Receiver Account Number: "))
        amount = float(input("Enter Transaction Amount: "))
        time = str( datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        location = input("Location: ")
        if sender not in self.accounts or receiver not in self.accounts:
            print("Invalid sender or receiver account.")
            return
        sender_acc = self.accounts[sender]
        transaction = TransactionWrapper(sender, receiver, amount, time, location, sender_acc.account.contents.locations)
        sender_acc.update_risk(transaction)
        self.graph.add_edge(self.nodes[sender], self.nodes[receiver], transaction)

    def display_accounts(self):
        print("\nAccounts:")
        for acc in self.accounts.values():
            acc.display()

    def display_graph(self):
        print("\nTransaction Graph:")
        self.graph.display()

    def run(self):
        while True:
            print("\nMenu:")
            print("1. Create Account")
            print("2. Create Transaction")
            print("3. Display Accounts")
            print("4. Display Transaction Graph")
            print("5. Go Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.create_transaction()
            elif choice == "3":
                self.display_accounts()
            elif choice == "4":
                self.display_graph()
            elif choice == "5":
                print("Going Back...")
                break
            else:
                print("Invalid choice. Try again.")
