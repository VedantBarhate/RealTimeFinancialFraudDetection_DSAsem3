#ifndef GRAPH_H
#define GRAPH_H

#include "account.h"
#include "transaction.h"

// Edge structure
typedef struct Edge
{
    int dest;
    transaction trans;
    struct Edge *next_edge;
} Edge;

// Node structure
typedef struct Node
{
    const account *acc;
    Edge *outgoing_edges;
    Edge *incoming_edges;
    struct Node *next_node;
} Node;

// Graph structure
typedef struct Graph
{
    int num_accounts;
    Node *first_node;
} Graph;

// Function declarations
Graph *create_graph();
Node *create_node(const account *acc);
void add_node(Graph *gr, Node *n);
void add_edge(Node *from_node, Node *to_node, transaction t);
void display_graph(Graph *gr);
void detect_fraudulent_transactions(Graph *gr);
void detect_sudden_large_transfers(Graph *gr);

#endif
