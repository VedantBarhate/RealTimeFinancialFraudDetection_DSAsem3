from transaction import TransactionWrapper
from account import AccountWrapper
from graph import GraphWrapper
from bst import BSTWrapper

import random
from datetime import datetime, timedelta

class Acting_DB:
    def __init__(self) -> None:
        self.accounts = {}
        self.nodes = {}
        self.transactions = []
        self.graph = GraphWrapper()
        self.bst = BSTWrapper()

        self.__fill_db()
        self.commit_nodes()

    def __fill_db(self):
        global account1, account2, account3, account4
        account1 = AccountWrapper(acc_num=101)
        account2 = AccountWrapper(acc_num=102)
        account3 = AccountWrapper(acc_num=103)
        account4 = AccountWrapper(acc_num=104)

        self.accounts[account1.account.contents.acc_num] = account1
        self.accounts[account2.account.contents.acc_num] = account2
        self.accounts[account3.account.contents.acc_num] = account3
        self.accounts[account4.account.contents.acc_num] = account4
        
        node1 = self.graph.add_node(account1)
        node2 = self.graph.add_node(account2)
        node3 = self.graph.add_node(account3)
        node4 = self.graph.add_node(account4)

        self.nodes = {
            101: node1, 
            102: node2, 
            103: node3,
            104: node4
        }

        self.transactions = self.generate_transactions(self.accounts, self.graph, self.nodes)
    
    def commit_nodes(self):
        self.bst.insert(account1)
        self.bst.insert(account2)
        self.bst.insert(account3)
        self.bst.insert(account4)

    @staticmethod
    def generate_transactions(accounts, graph, nodes, num_transactions=200):
        account1 = accounts[101]
        account2 = accounts[102]
        account3 = accounts[103]
        account4 = accounts[104]
        transactions = []
        locations = [
            "Mumbai", "Delhi", "Bangalore", "Chennai"
            # "Kolkata", "Pune", "Hyderabad", "Jaipur" 
            # "Ahmedabad", "Surat", "Lucknow", "Patna"
        ]
        amount_ranges = [
            (1, 100),
            (1, 100),
            (1, 100),
            (1, 100),
            (1, 100),
            (1, 100),
            (1, 100),
            (1, 100),
            (1, 100),
            (1, 100),
            (100, 500),
            (100, 500),
            (100, 500),
            (100, 500),
            (100, 500),
            (100, 500),
            (100, 500),
            (100, 500),
            (100, 500),
            (100, 500),
            (500, 1000),
            (500, 1000),   
            (1000, 2000),  
            (1000, 2000),
            (5000, 10000)
        ]
        account_combinations = [
            (account1, account2, nodes[101], nodes[102]),
            (account1, account3, nodes[101], nodes[103]),
            (account1, account4, nodes[101], nodes[104]),
            (account2, account1, nodes[102], nodes[101]),
            (account2, account3, nodes[102], nodes[103]),
            (account2, account4, nodes[102], nodes[104]),
            (account3, account1, nodes[103], nodes[101]),
            (account3, account2, nodes[103], nodes[102]),
            (account3, account4, nodes[103], nodes[104]),
            (account4, account1, nodes[104], nodes[101]),
            (account4, account2, nodes[104], nodes[102]),
            (account4, account3, nodes[104], nodes[103])
        ]

        base_date = datetime(2024, 1, 1)
        for i in range(num_transactions):
            sender_account, receiver_account, sender_node, receiver_node = random.choice(account_combinations)
            min_amount, max_amount = random.choice(amount_ranges)
            amount = int(round(random.uniform(min_amount, max_amount), 2))
            transaction_time = base_date + timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            time_str = transaction_time.strftime("%Y-%m-%d_%H:%M:%S")
            location = random.choice(locations)
            transaction = TransactionWrapper(
                sender=sender_account.account.contents.acc_num,
                receiver=receiver_account.account.contents.acc_num,
                amount=amount,
                time=time_str,
                location=location,
                loc_freq_array=sender_account.account.contents.locations
            )
            sender_account.update_risk(transaction)
            graph.add_edge(sender_node, receiver_node, transaction)
            transactions.append(transaction)
        return transactions