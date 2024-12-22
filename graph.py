import ctypes
from ctypes import Structure, c_int, c_float, c_double, POINTER

from account import AccountWrapper, Account
from transaction import TransactionWrapper, Transaction


# Load the shared library for the graph
graph_lib = ctypes.CDLL('dlls/graph.dll')


# Define the Edge structure
class Edge(Structure):
    _fields_ = [
        ("dest", c_int),
        ("trans", Transaction),
        ("next_edge", POINTER("Edge")),
    ]


# Define the Node structure
class Node(Structure):
    _fields_ = [
        ("acc", POINTER(Account)),
        ("outgoing_edges", POINTER(Edge)),
        ("incoming_edges", POINTER(Edge)),
        ("next_node", POINTER("Node")),
    ]


# Define the Graph structure
class Graph(Structure):
    _fields_ = [
        ("num_accounts", c_int),
        ("first_node", POINTER(Node)),
    ]


# Define function signatures for the C functions
graph_lib.create_graph.argtypes = []
graph_lib.create_graph.restype = POINTER(Graph)

graph_lib.create_node.argtypes = [POINTER(Account)]
graph_lib.create_node.restype = POINTER(Node)

graph_lib.add_node.argtypes = [POINTER(Graph), POINTER(Node)]
graph_lib.add_node.restype = None

graph_lib.add_edge.argtypes = [POINTER(Node), POINTER(Node), Transaction]
graph_lib.add_edge.restype = None

graph_lib.display_graph.argtypes = [POINTER(Graph)]
graph_lib.display_graph.restype = None

graph_lib.detect_fraudulent_transactions.argtypes = [POINTER(Graph)]
graph_lib.detect_fraudulent_transactions.restype = None

graph_lib.detect_sudden_large_transfers.argtypes = [POINTER(Graph)]
graph_lib.detect_sudden_large_transfers.restype = None


# Python OOP Wrapper for Graph
class GraphWrapper:
    def __init__(self):
        self.graph = graph_lib.create_graph()

    def add_node(self, account):
        """
        Add a node to the graph with the given account.
        """
        node = graph_lib.create_node(account.account)
        graph_lib.add_node(self.graph, node)
        return node

    def add_edge(self, from_node, to_node, transaction):
        """
        Add an edge between two nodes with the given transaction.
        """
        graph_lib.add_edge(from_node, to_node, transaction.transaction)

    def display(self):
        """
        Display the entire graph structure.
        """
        graph_lib.display_graph(self.graph)

    def detect_fraudulent_transactions(self):
        """
        Detect potential fraudulent transactions.
        """
        graph_lib.detect_fraudulent_transactions(self.graph)

    def detect_sudden_large_transfers(self):
        """
        Detect sudden large transfers in the graph.
        """
        graph_lib.detect_sudden_large_transfers(self.graph)


# Example usage
if __name__ == "__main__":
    # Create accounts
    account1 = AccountWrapper(acc_num=101)
    account2 = AccountWrapper(acc_num=102)

    # Create transactions
    transaction1 = TransactionWrapper(
        sender=account1.account.contents.acc_num,
        receiver=account2.account.contents.acc_num,
        amount=6000.0,
        time="2024-11-16_12:30:45",
        location="Mumbai",
        loc_freq_array=account1.account.contents.locations,
    )

    transaction2 = TransactionWrapper(
        sender=account1.account.contents.acc_num,
        receiver=account2.account.contents.acc_num,
        amount=2000.0,
        time="2024-11-16_13:30:45",
        location="Pune",
        loc_freq_array=account2.account.contents.locations,
    )

    # Create a graph
    graph = GraphWrapper()

    # Add nodes to the graph
    node1 = graph.add_node(account1)
    node2 = graph.add_node(account2)

    # Add edges to the graph
    graph.add_edge(node1, node2, transaction1)
    graph.add_edge(node1, node2, transaction2)

    # Display the graph
    graph.display()

    # Detect fraudulent transactions
    graph.detect_fraudulent_transactions()

    # Detect sudden large transfers
    graph.detect_sudden_large_transfers()
