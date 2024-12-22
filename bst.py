import ctypes
from ctypes import Structure, POINTER, c_char_p

from account import AccountWrapper, Account


# Load the shared library for BST
bst_lib = ctypes.CDLL('dlls/bst.dll')


# Define the BST Node structure
class BSTNode(Structure):
    _fields_ = [
        ("acc", POINTER(Account)),
        ("flag", c_char_p),
        ("left", POINTER("BSTNode")),
        ("right", POINTER("BSTNode")),
    ]


# Add a self-referential structure definition
BSTNode._fields_[2] = ("left", POINTER(BSTNode))
BSTNode._fields_[3] = ("right", POINTER(BSTNode))


# Define function signatures for the C functions
bst_lib.create_bst_node.argtypes = [POINTER(Account)]
bst_lib.create_bst_node.restype = POINTER(BSTNode)

bst_lib.insert.argtypes = [POINTER(BSTNode), POINTER(Account)]
bst_lib.insert.restype = POINTER(BSTNode)

bst_lib.inorder_traverse.argtypes = [POINTER(BSTNode)]
bst_lib.inorder_traverse.restype = None

bst_lib.targeted_monitoring.argtypes = [POINTER(BSTNode)]
bst_lib.targeted_monitoring.restype = None


# Python wrapper for the BSTNode and operations
class BSTWrapper:
    def __init__(self):
        self.root = None

    def create_node(self, account):
        """
        Create a new BST node for the given account.
        """
        return bst_lib.create_bst_node(account.account)

    def insert(self, account):
        """
        Insert an account into the BST based on risk score.
        """
        account_pointer = account.account
        self.root = bst_lib.insert(self.root, account_pointer)

    def inorder_traverse(self):
        """
        Perform an in-order traversal of the BST.
        """
        print("In-order Traversal of BST:")
        bst_lib.inorder_traverse(self.root)

    def targeted_monitoring(self):
        """
        Perform targeted monitoring to flag accounts based on risk score.
        """
        print("Targeted Monitoring:")
        bst_lib.targeted_monitoring(self.root)


# Example usage
if __name__ == "__main__":
    # Create accounts
    account1 = AccountWrapper(acc_num=101)
    account2 = AccountWrapper(acc_num=102)
    account3 = AccountWrapper(acc_num=103)

    # Modify risk scores for demonstration (assuming these functions exist in account.dll)
    account1.account.contents.acc_risk_score = 0.85
    account2.account.contents.acc_risk_score = 0.45
    account3.account.contents.acc_risk_score = 0.95

    # Create a BST and insert accounts
    bst = BSTWrapper()
    bst.insert(account1)
    bst.insert(account2)
    bst.insert(account3)

    # Traverse the BST
    bst.inorder_traverse()

    # Perform targeted monitoring
    bst.targeted_monitoring()
