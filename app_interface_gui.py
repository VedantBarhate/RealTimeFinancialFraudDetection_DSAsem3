import customtkinter as ctk
from account import AccountWrapper
from transaction import TransactionWrapper
from graph import GraphWrapper
from bst import BSTWrapper
from datetime import datetime
from acting_db import Acting_DB
import os
import tempfile
from datetime import datetime


def display_graph(self):
    self.clear_content_frame()
    ctk.CTkLabel(self.content_frame, text="Transaction Graph", font=("Arial", 18)).pack(pady=10)

    # Redirect C stdout
    temp_output = tempfile.TemporaryFile(mode='w+')
    fd = temp_output.fileno()
    old_stdout = os.dup(1)  # Duplicate the file descriptor for stdout (fd 1)
    os.dup2(fd, 1)  # Redirect fd 1 (stdout) to our temporary file

    try:
        self.graph.display()  # Call the graph display method
    finally:
        os.dup2(old_stdout, 1)  # Restore the original stdout
        os.close(old_stdout)

    # Read captured output
    temp_output.seek(0)  # Move to the beginning of the file
    graph_info = temp_output.read()
    temp_output.close()

    if not graph_info.strip():
        graph_info = "No graph data available."

    # Display the graph information in the GUI
    graph_textbox = ctk.CTkTextbox(self.content_frame, width=500, height=300)
    graph_textbox.insert("1.0", graph_info)
    graph_textbox.pack(pady=10)
    graph_textbox.configure(state="disabled")

class AppInterfaceGUI(ctk.CTk):
    def __init__(self, db: Acting_DB):
        super().__init__()

        # Set window properties
        self.title("App Interface")
        self.geometry("800x800")
        # self.resizable(False, False)

        # Database and components
        self.db = db
        self.accounts = None
        self.nodes = None
        self.graph: GraphWrapper = None
        self.bst: BSTWrapper = None
        self.__load_data_from_db()

        # UI elements
        self.create_widgets()

    def __load_data_from_db(self):
        self.accounts = self.db.accounts
        self.nodes = self.db.nodes
        self.graph = self.db.graph
        self.bst = self.db.bst

    def create_widgets(self):
        # Create menu buttons
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.pack(side="right", expand=True, fill=ctk.BOTH, padx=10, pady=10)

        ctk.CTkButton(self.menu_frame, text="Create Account", command=self.create_account).pack(pady=10)
        ctk.CTkButton(self.menu_frame, text="Create Transaction", command=self.create_transaction).pack(pady=10)
        ctk.CTkButton(self.menu_frame, text="Display Accounts", command=self.display_accounts).pack(pady=10)
        ctk.CTkButton(self.menu_frame, text="Display Transaction Graph", command=self.display_graph).pack(pady=10)
        ctk.CTkButton(self.menu_frame, text="Exit", command=self.destroy).pack(pady=10)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_account(self):
        def save_account():
            acc_num = int(acc_num_entry.get())
            if acc_num in self.accounts:
                status_label.configure(text="Account already exists!", fg_color="red")
                return
            account = AccountWrapper(acc_num)
            self.accounts[acc_num] = account
            node = self.graph.add_node(account)
            self.nodes[acc_num] = node
            self.bst.insert(account)
            status_label.configure(text="Account created successfully!", fg_color="green")

        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Create Account", font=("Arial", 18)).pack(pady=10)
        acc_num_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Account Number")
        acc_num_entry.pack(pady=10)
        ctk.CTkButton(self.content_frame, text="Save", command=save_account).pack(pady=10)
        status_label = ctk.CTkLabel(self.content_frame, text="")
        status_label.pack(pady=10)

    def create_transaction(self):
        def save_transaction():
            try:
                sender = int(sender_entry.get())
                receiver = int(receiver_entry.get())
                amount = float(amount_entry.get())
                time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                location = location_entry.get()

                if sender not in self.accounts or receiver not in self.accounts:
                    status_label.configure(text="Invalid sender or receiver account.", fg_color="red")
                    return

                sender_acc = self.accounts[sender]
                transaction = TransactionWrapper(sender, receiver, amount, time, location, sender_acc.account.contents.locations)
                sender_acc.update_risk(transaction)
                self.graph.add_edge(self.nodes[sender], self.nodes[receiver], transaction)
                status_label.configure(text="Transaction created successfully!", fg_color="green")
            except ValueError:
                status_label.configure(text="Invalid input values.", fg_color="red")

        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Create Transaction", font=("Arial", 18)).pack(pady=10)

        sender_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Sender Account Number")
        sender_entry.pack(pady=10)

        receiver_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Receiver Account Number")
        receiver_entry.pack(pady=10)

        amount_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Transaction Amount")
        amount_entry.pack(pady=10)

        location_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Transaction Location")
        location_entry.pack(pady=10)

        ctk.CTkButton(self.content_frame, text="Save", command=save_transaction).pack(pady=10)
        status_label = ctk.CTkLabel(self.content_frame, text="")
        status_label.pack(pady=10)

    def display_accounts(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Accounts", font=("Arial", 18)).pack(pady=10)
        if not self.accounts:
            ctk.CTkLabel(self.content_frame, text="No accounts available.").pack(pady=10)
            return
        for acc in self.accounts.values():
            acc_label = ctk.CTkLabel(self.content_frame, text=str(acc))
            acc_label.pack(pady=5)


    def display_graph(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Transaction Graph", font=("Arial", 18)).pack(pady=10)

        # Redirect C stdout
        temp_output = tempfile.TemporaryFile(mode='w+')
        fd = temp_output.fileno()
        old_stdout = os.dup(1)  # Duplicate the file descriptor for stdout (fd 1)
        os.dup2(fd, 1)  # Redirect fd 1 (stdout) to our temporary file

        try:
            self.graph.display()  # Call the graph display method
        finally:
            os.dup2(old_stdout, 1)  # Restore the original stdout
            os.close(old_stdout)

        # Read captured output
        temp_output.seek(0)  # Move to the beginning of the file
        graph_info = temp_output.read()
        temp_output.close()

        if not graph_info.strip():
            graph_info = "No graph data available."

        # Display the graph information in the GUI
        graph_textbox = ctk.CTkTextbox(self.content_frame, width=500, height=300)
        graph_textbox.insert("1.0", graph_info)
        graph_textbox.pack(pady=10, fill=ctk.BOTH, expand=True)
        graph_textbox.configure(state="disabled")


if __name__ == "__main__":
    db = Acting_DB()  # Replace with actual database initialization
    app = AppInterfaceGUI(db)
    app.mainloop()
