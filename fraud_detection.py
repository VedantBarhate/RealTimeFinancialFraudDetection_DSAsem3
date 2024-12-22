from graph import GraphWrapper
from bst import BSTWrapper

class FraudDetection:
    def __init__(self, graph: GraphWrapper, bst: BSTWrapper):
        self.graph = graph
        self.bst = bst

    # graph algos
    def detect_fraudulent_transactions(self):
        self.graph.detect_fraudulent_transactions()

    def detect_sudden_large_transfers(self):
        self.graph.detect_sudden_large_transfers()

    # bst algos
    def inorder_traversal(self):
        
        self.bst.inorder_traverse()

    def targeted_monitoring(self):
        self.bst.targeted_monitoring()
    
    def run(self):
        while True:
            print("\nMenu:")
            print("1. Detect Fraudulent Transactions")
            print("2. Detect Sudden Large Transfers")
            print("3. Inorder Traversal")
            print("4. Targeted Monitoring")
            print("5. Go Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.detect_fraudulent_transactions()
            elif choice == "2":
                self.detect_sudden_large_transfers()
            elif choice == "3":
                self.inorder_traversal()
            elif choice == "4":
                self.targeted_monitoring()
            elif choice == "5":
                print("Going Back...")
                break
            else:
                print("Invalid choice. Try again.")
