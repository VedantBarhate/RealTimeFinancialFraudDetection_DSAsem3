import customtkinter as ctk
import os
import sys
import tempfile
import msvcrt
from io import StringIO
# from graph import GraphWrapper
# from bst import BSTWrapper
from acting_db import Acting_DB


class DualOutput:
    def __init__(self, original_stdout):
        self.console = original_stdout
        self.buffer = StringIO()

    def write(self, message):
        # Write to console
        self.console.write(message)
        self.console.flush()
        # Write to buffer
        self.buffer.write(message)

    def flush(self):
        self.console.flush()
        self.buffer.flush()

    def get_output(self):
        return self.buffer.getvalue()


class FraudDetectionGUI(ctk.CTk):
    def __init__(self, db : Acting_DB):
        super().__init__()
        self.db = db
        self.graph = db.graph
        self.bst = db.bst

        # Window setup
        self.title("Fraud Detection System")
        self.geometry("800x800")

        # Title label
        self.title_label = ctk.CTkLabel(self, text="Fraud Detection System", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # Output textbox
        self.output_textbox = ctk.CTkTextbox(self, height=300, wrap="word", font=("Arial", 12))
        self.output_textbox.pack(padx=20, pady=10, fill="both", expand=True)

        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.fraud_button = ctk.CTkButton(self.button_frame, text="Detect Fraudulent Transactions",
                                         command=self.detect_fraudulent_transactions)
        self.fraud_button.grid(row=0, column=0, padx=10, pady=5)

        self.large_transfers_button = ctk.CTkButton(self.button_frame, text="Detect Sudden Large Transfers",
                                                    command=self.detect_sudden_large_transfers)
        self.large_transfers_button.grid(row=0, column=1, padx=10, pady=5)

        self.inorder_button = ctk.CTkButton(self.button_frame, text="Inorder Traversal", 
                                           command=self.inorder_traversal)
        self.inorder_button.grid(row=1, column=0, padx=10, pady=5)

        self.monitoring_button = ctk.CTkButton(self.button_frame, text="Targeted Monitoring",
                                               command=self.targeted_monitoring)
        self.monitoring_button.grid(row=1, column=1, padx=10, pady=5)

        self.quit_button = ctk.CTkButton(self.button_frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def display_output_textbox(self, output):
        """
        Display the captured output in the GUI textbox.
        """
        self.output_textbox.delete("1.0", "end")  # Clear previous content
        self.output_textbox.insert("1.0", output)  # Insert new output
        self.output_textbox.see("end")  # Scroll to the end

    def capture_c_output(self, function):
        """
        Capture C stdout (printf) output while also printing to the console.
        """
        # Create a temporary file for C output redirection
        temp_output = tempfile.TemporaryFile(mode='w+t')
        fd_temp = temp_output.fileno()

        # Save the original stdout
        original_stdout_fd = sys.stdout.fileno()
        saved_stdout = os.dup(original_stdout_fd)
        original_stdout = sys.stdout

        # Create a dual output stream
        dual_output = DualOutput(original_stdout)

        try:
            # Redirect stdout to both temp file and dual output
            os.dup2(fd_temp, original_stdout_fd)
            msvcrt.setmode(original_stdout_fd, os.O_TEXT)
            sys.stdout = dual_output  # Redirect Python stdout to DualOutput

            # Call the C function (which prints to stdout)
            function()

            # Flush and rewind the temp file to capture C output
            sys.stdout.flush()
            temp_output.seek(0)
            c_output = temp_output.read()

            # Print C output to console and buffer
            dual_output.write(c_output)

        finally:
            # Restore original stdout
            os.dup2(saved_stdout, original_stdout_fd)
            os.close(saved_stdout)
            sys.stdout = original_stdout
            temp_output.close()

        # Return combined output
        return dual_output.get_output()

    def detect_fraudulent_transactions(self):
        self.graph.detect_fraudulent_transactions()

    def detect_sudden_large_transfers(self):
        self.graph.detect_sudden_large_transfers()

    def inorder_traversal(self):
        self.bst.inorder_traverse()

    def targeted_monitoring(self):
        self.bst.targeted_monitoring()


if __name__ == "__main__":
    db = Acting_DB()

    app = FraudDetectionGUI(db)
    app.mainloop()
