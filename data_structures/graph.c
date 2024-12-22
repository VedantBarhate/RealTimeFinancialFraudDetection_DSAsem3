#include <stdlib.h>
#include <stdio.h>
#include "graph.h"
// #include "account.h"
// #include "transaction.h"

// Function to create a new graph
Graph *create_graph()
{
    Graph *gr = (Graph *)malloc(sizeof(Graph));
    gr->num_accounts = 0;
    gr->first_node = NULL;
    return gr;
}

// Function to create a new node in the graph
Node *create_node(const account *acc)
{
    Node *n = (Node *)malloc(sizeof(Node));
    n->acc = acc;
    n->outgoing_edges = NULL;
    n->incoming_edges = NULL;
    n->next_node = NULL;
    return n;
}

// Function to add a node to the graph
void add_node(Graph *gr, Node *n)
{
    gr->num_accounts++;
    if (gr->first_node == NULL)
    {
        gr->first_node = n;
    }
    else
    {
        Node *current = gr->first_node;
        while (current->next_node != NULL)
        {
            current = current->next_node;
        }
        current->next_node = n;
    }
}

// Function to add an edge between two nodes
void add_edge(Node *from_node, Node *to_node, transaction t)
{
    // Outgoing edge from the 'from_node' to 'to_node'
    Edge *new_edge = (Edge *)malloc(sizeof(Edge));
    new_edge->dest = to_node->acc->acc_num;
    new_edge->trans = t;
    new_edge->next_edge = from_node->outgoing_edges;
    from_node->outgoing_edges = new_edge;

    // Incoming edge to the 'to_node' from 'from_node'
    Edge *incoming_edge = (Edge *)malloc(sizeof(Edge));
    incoming_edge->dest = from_node->acc->acc_num;
    incoming_edge->trans = t;
    incoming_edge->next_edge = to_node->incoming_edges;
    to_node->incoming_edges = incoming_edge;
}

// Helper function to display edges
void display_edge(Edge *e)
{
    while (e != NULL)
    {
        display_transaction(&e->trans);
        e = e->next_edge;
    }
}

// Function to display a node's information
void display_node(Node *n)
{
    printf("Account %d (Risk Score: %.2f):\n", n->acc->acc_num, n->acc->acc_risk_score);
    display_account(n->acc);
    printf("    Outgoing transactions:\n");
    display_edge(n->outgoing_edges);
    printf("    Incoming transactions:\n");
    display_edge(n->incoming_edges);
}

// Function to display the entire graph
void display_graph(Graph *gr)
{
    printf("Number of accounts: %d\n", gr->num_accounts);
    Node *current = gr->first_node;
    while (current != NULL)
    {
        display_node(current);
        printf("\n");
        current = current->next_node;
    }
}

// Function to detect fraudulent transactions
void detect_fraudulent_transactions(Graph *gr)
{
    Node *current = gr->first_node;
    while (current != NULL)
    {
        Edge *out_edge = current->outgoing_edges;
        float avg_trans_amount = current->acc->avg_trans_amnt; // Average transaction amount for the account

        while (out_edge != NULL)
        {
            // Criteria for fraud detection
            if (out_edge->trans.amount > avg_trans_amount * 2 ||  // Sudden large transaction
                out_edge->trans.amount > 10000 ||                 // Very high transaction amount
                (current->acc->acc_risk_score > 0.75 &&           // High-risk account
                 out_edge->trans.amount > 5000))
            {
                printf("Fraudulent Transaction Detected! Transaction from %d to %d with amount %.2f (Risk Score: %.2f)\n",
                       out_edge->trans.sender, out_edge->trans.receiver, out_edge->trans.amount, current->acc->acc_risk_score);
            }

            // Additional anomaly: Large transaction for a low-risk account
            if (current->acc->acc_risk_score < 0.3 && out_edge->trans.amount > avg_trans_amount * 2.5)
            {
                printf("Anomaly Detected! Low-risk account %d initiated a large transaction to %d with amount %.2f (Threshold: %.2f)\n",
                       out_edge->trans.sender, out_edge->trans.receiver, out_edge->trans.amount, avg_trans_amount * 2.0);
            }

            out_edge = out_edge->next_edge;
        }

        current = current->next_node;
    }
}


void detect_sudden_large_transfers(Graph *gr)
{
    Node *current = gr->first_node;
    while (current != NULL)
    {
        Edge *out_edge = current->outgoing_edges;
        float avg_trans_amount = current->acc->avg_trans_amnt;

        while (out_edge != NULL)
        {
            if (out_edge->trans.amount > avg_trans_amount * 1.5)
            {
                printf("Sudden Large Transfer Detected! Transaction from %d to %d with amount %.2f (Threshold: %.2f)\n",
                       out_edge->trans.sender, out_edge->trans.receiver, out_edge->trans.amount, avg_trans_amount * 1.5);
            }
            out_edge = out_edge->next_edge;
        }
        current = current->next_node;
    }
}

// detect_unusual_transaction_path