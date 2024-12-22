import ctypes
from ctypes import Structure, c_int, c_float, c_double, c_char_p, POINTER
from loc_freq import LocationFrequencyArray, LocFreqArray
from transaction import Transaction, TransactionWrapper

# Load the shared library for account
account_lib = ctypes.CDLL('dlls/account.dll')

# Define the Account structure
class Account(Structure):
    _fields_ = [
        ("acc_num", c_int),
        ("no_of_transactions", c_int),
        ("avg_trans_amnt", c_double),
        ("avg_trans_risk_score", c_double),
        ("locations", LocFreqArray),
        ("acc_risk_score", c_double),
    ]

# Define function signatures for C functions
account_lib.create_account.argtypes = [c_int]
account_lib.create_account.restype = POINTER(Account)

# account_lib.calculate_location_risk.argtypes = [POINTER(LocFreqArray), c_char_p]
# account_lib.calculate_location_risk.restype = c_float

account_lib.update_account_risk.argtypes = [POINTER(Account), POINTER(Transaction)]
account_lib.update_account_risk.restype = None

account_lib.display_account.argtypes = [POINTER(Account)]
account_lib.display_account.restype = None

# Python OOP Wrapper for Account
class AccountWrapper:
    def __init__(self, acc_num):
        self.account = account_lib.create_account(acc_num)

    def update_risk(self, transaction):
        """
        Update the account's risk score based on a given transaction.
        """
        account_lib.update_account_risk(self.account, ctypes.byref(transaction.transaction))

    def display(self):
        """
        Display the account details.
        """
        account_lib.display_account(self.account)
        print("\n")

    def __repr__(self):
        return (
            f"Account(acc_num={self.account.contents.acc_num}, "
            f"no_of_transactions={self.account.contents.no_of_transactions}, "
            f"avg_trans_amnt={self.account.contents.avg_trans_amnt:.2f}, "
            f"avg_trans_risk_score={self.account.contents.avg_trans_risk_score:.2f}, "
            f"acc_risk_score={self.account.contents.acc_risk_score:.2f})"
        )

# Example usage
if __name__ == "__main__":
    # Create a LocationFrequencyArray
    loc_freq_array = LocationFrequencyArray()
    # loc_freq_array.add("New York", 5)
    # loc_freq_array.add("San Francisco", 3)

    # Create a Transaction
    transaction1 = TransactionWrapper(sender=1,
                                    receiver=2, 
                                    amount=1550.0, 
                                    time="2024-11-16_12:30:45", 
                                    location="Mumbai", 
                                    loc_freq_array=loc_freq_array.array)
    
    transaction2 = TransactionWrapper(sender=1,
                                    receiver=2, 
                                    amount=50.0, 
                                    time="2024-11-16_12:30:45", 
                                    location="Mumbai", 
                                    loc_freq_array=loc_freq_array.array)
    
    transaction3 = TransactionWrapper(sender=1,
                                    receiver=2, 
                                    amount=3050.0, 
                                    time="2024-11-16_12:30:45", 
                                    location="Pune", 
                                    loc_freq_array=loc_freq_array.array)

    # Create an Account
    account = AccountWrapper(acc_num=101)

    # Update account risk with the transaction
    account.update_risk(transaction1)
    account.update_risk(transaction2)
    account.update_risk(transaction3)

    # Display the account details
    account.display()
