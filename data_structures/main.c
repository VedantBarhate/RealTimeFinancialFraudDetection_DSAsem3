#include <stdio.h>
#include <stdlib.h>

#include "transaction.h"
#include "loc_freq.h"
#include "account.h"
#include "graph.h"
#include "bst.h"

int main()
{
    // Creating a graph to hold accounts and transactions
    Graph *gr = create_graph();

    // Create accounts
    account *a1 = create_account(1001);
    account *a2 = create_account(1002);
    account *a3 = create_account(1003);
    account *a4 = create_account(1004);

    // Add accounts as nodes in the graph
    Node *n1 = create_node(a1); //ach
    Node *n2 = create_node(a2); //dokodo
    Node *n3 = create_node(a3); //vib
    Node *n4 = create_node(a4); //shri

    add_node(gr, n1);
    add_node(gr, n2);
    add_node(gr, n3);
    add_node(gr, n4);

    // Create transactions and add edges to the graph
    transaction t1 = create_transaction(a1->acc_num, a2->acc_num, 5000, "19-8-2024_16:19:55", "Pune", &a1->locations);
    update_account_risk(a1, &t1);
    transaction t2 = create_transaction(a1->acc_num, a3->acc_num, 20000, "29-8-2024_13:09:20", "Pune", &a1->locations);
    update_account_risk(a1, &t2);
    transaction t3 = create_transaction(a2->acc_num, a3->acc_num, 5820, "12-9-2024_21:10:42", "Mumbai", &a2->locations);
    update_account_risk(a2, &t3);
    transaction t4 = create_transaction(a3->acc_num, a1->acc_num, 150, "17-7-2024_22:36:02", "Mumbai", &a3->locations);
    update_account_risk(a3, &t4);

    add_edge(n1, n2, t1);
    add_edge(n1, n3, t2);
    add_edge(n2, n3, t3);
    add_edge(n3, n1, t4);

    // Display the graph with accounts and their transactions
    printf("Displaying Graph:\n");
    display_graph(gr);

    printf("\nDetection for Fradulent Transactions:\n");
    detect_fraudulent_transactions(gr);

    printf("\nDetection for sudden large transfers:\n");
    detect_sudden_large_transfers(gr);


    printf("\nBST ...\n");
    // creating a BST for targeted monitoring
    bst_node *root = NULL;

    // Insert accounts into the BST based on risk score
    root = insert(root, a1);
    root = insert(root, a2);
    root = insert(root, a3);
    root = insert(root, a4);

    printf("\ntargeted monitoring...\n");
    targeted_monitoring(root);

    // Traverse and display the BST in order (sorted by risk score)
    printf("\nDisplaying Accounts Sorted by Risk Score (BST In-order Traversal):\n");
    inorder_traverse(root);
    return 0;
}