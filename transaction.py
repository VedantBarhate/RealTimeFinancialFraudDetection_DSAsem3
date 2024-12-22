import ctypes
from ctypes import Structure, c_int, c_float, c_char, c_char_p, POINTER
from loc_freq import LocationFrequencyArray, LocFreqArray
from loc_freq import LocationFrequencyArray

# Load the transaction shared library
transaction_lib = ctypes.CDLL('dlls/transaction.dll')

# Define the transaction structure
class Transaction(Structure):
    _fields_ = [
        ("sender", c_int),
        ("receiver", c_int),
        ("amount", c_float),
        ("time", c_char * 19),  # Format: YYYY-MM-DD_HH:MM:SS
        ("location", c_char * 30),
        ("trans_risk_score", c_float),
    ]

# Define function signatures for C functions
transaction_lib.calculate_trans_risk.argtypes = [c_float, c_char_p, c_char_p, POINTER(LocFreqArray)]
transaction_lib.calculate_trans_risk.restype = c_float

transaction_lib.create_transaction.argtypes = [c_int, c_int, c_float, c_char_p, c_char_p, POINTER(LocFreqArray)]
transaction_lib.create_transaction.restype = Transaction

transaction_lib.display_transaction.argtypes = [POINTER(Transaction)]
transaction_lib.display_transaction.restype = None

# Python OOP Wrapper for Transaction
class TransactionWrapper:
    def __init__(self, sender, receiver, amount, time, location, loc_freq_array):
        self.transaction = transaction_lib.create_transaction(
            sender, receiver, amount, time.encode('utf-8'), location.encode('utf-8'), ctypes.byref(loc_freq_array)
        )

    def display(self):
        transaction_lib.display_transaction(ctypes.byref(self.transaction))

    def __repr__(self):
        return (
            f"Transaction(sender={self.transaction.sender}, "
            f"receiver={self.transaction.receiver}, "
            f"amount={self.transaction.amount}, "
            f"time='{self.transaction.time.decode('utf-8')}', "
            f"location='{self.transaction.location.decode('utf-8')}', "
            f"risk_score={self.transaction.trans_risk_score})"
        )

# Example usage
if __name__ == "__main__":
    loc_freq_array = LocationFrequencyArray()
    loc_freq_array.add("New York", 5)
    loc_freq_array.add("San Francisco", 3)

    # Create a transaction
    transaction = TransactionWrapper(sender=1,
                                    receiver=2, 
                                    amount=1550.0, 
                                    time="2024-11-16_12:30:45", 
                                    location="Mumbai", 
                                    loc_freq_array=loc_freq_array.array)

    # Display transaction
    transaction.display()
    print(transaction)