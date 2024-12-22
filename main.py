from app_interface import AppInterface
from fraud_detection import FraudDetection
from acting_db import Acting_DB

def main():
    print("Welcome to the Real-Time Financial Fraud Detection System!\n")

    db = Acting_DB()
    app = AppInterface(db)

    fraud_detection = FraudDetection(app.graph, app.bst)

    while True:
        print("\nMain Menu:")
        print("1. Manage Accounts and Transactions")
        print("2. Run Algorithms")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            app.run()
        elif choice == "2":
            fraud_detection.run()
        elif choice == "3":
            print("Exiting the system...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()